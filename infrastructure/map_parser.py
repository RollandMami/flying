from abc import ABC, abstractmethod
from typing import Any


class ParserError(ValueError):
    def __init__(
            self,
            line_num: int,
            line_content: str,
            cause: str) -> None:
        self.line_num = line_num
        self.line_content = line_content
        self.cause = cause
        msg1 = f"Parse error at line {line_num}: {cause}"
        msg2 = f" (line: '{line_content}')"
        super().__init__(msg1 + msg2)


class BaseParser(ABC):
    @abstractmethod
    def load(self, path: str) -> dict[str, Any]:
        ...


class TxtParser(BaseParser):

    _VALID_ZONES: set[str] = {"normal", "blocked", "restricted", "priority"}
    _CAPACITY_KEYS: set[str] = {"max_drones", "max_link_capacity"}

    def __init__(self) -> None:
        self._path: str | None = None
        self._result: dict[str, Any] = {}
        self._keys: set[str] = {
            "nb_drones",
            "start_hub",
            "hub",
            "end_hub",
            "connection"
        }

    def set_path(self, path: str) -> None:
        if not path or len(path) <= 2:
            raise ValueError(f"Path errror : {path}")
        self._path = path

    @staticmethod
    def parse_options(text: str,
                      line_num: int,
                      line_content: str) -> dict[str, Any]:
        text = text.strip()
        if not text:
            return {}
        text = text.replace("[", "").replace("]", "")

        options: dict[str, Any] = {}
        for pair in text.split():
            if "=" not in pair:
                raise ParserError(
                    line_num, line_content,
                    f"invalid metadata token '{pair}', expected 'key=value'"
                )
            key, value = pair.split("=", 1)
            key, value = key.strip(), value.strip()
            if not key or not value:
                raise ParserError(line_num,
                                  line_content,
                                  f"invalid metadata token '{pair}'")

            if key == "zone":
                if value not in TxtParser._VALID_ZONES:
                    raise ParserError(
                        line_num, line_content,
                        f"invalid zone type '{value}', expected one of "
                        f"{sorted(TxtParser._VALID_ZONES)}"
                    )
                options[key] = value

            elif key in TxtParser._CAPACITY_KEYS:
                if not value.lstrip("-").isdigit():
                    raise ParserError(
                        line_num,
                        line_content,
                        f"'{key}' must be an int, got '{value}'"
                    )
                int_value = int(value)
                if int_value <= 0:
                    raise ParserError(
                        line_num, line_content,
                        f"'{key}' must be a positive int, got {int_value}"
                    )
                options[key] = int_value

            else:
                if value.lstrip("-").isdigit():
                    options[key] = int(value)
                else:
                    options[key] = value
        return options

    def _split_head_and_options(self, arg: str) -> tuple[str, str]:
        index = arg.find("[")
        if index == -1:
            return arg.strip(), ""
        return arg[:index].strip(), arg[index:].strip()

    def parse_hub_line(self,
                       arg: str,
                       line_num: int,
                       line_content: str) -> dict[str, Any]:
        head, opts_str = self._split_head_and_options(arg)
        tokens = head.split()
        if len(tokens) < 3:
            raise ParserError(
                line_num,
                line_content,
                "expected format '<name> <x> <y>'"
            )
        name = tokens[0]
        if "-" in name:
            raise ParserError(
                line_num,
                line_content,
                f"zone name must not contain '-': '{name}'"
            )
        try:
            x, y = int(tokens[1]), int(tokens[2])
        except ValueError:
            raise ParserError(
                line_num, line_content,
                f"coordinates must be int, got '{tokens[1]}' '{tokens[2]}'"
            ) from None

        return {
            "name": name,
            "x": x,
            "y": y,
            "meta": self.parse_options(opts_str, line_num, line_content),
        }

    def parse_connection_line(self,
                              arg: str,
                              line_num: int,
                              line_content: str) -> dict[str, Any]:
        head, opts_str = self._split_head_and_options(arg)
        if "-" not in head:
            raise ParserError(
                line_num, line_content, "expected format '<zone1>-<zone2>'"
            )
        left, right = head.split("-", 1)
        left, right = left.strip(), right.strip()
        if not left or not right:
            raise ParserError(line_num,
                              line_content,
                              "connection zone names must not be empty")

        data: dict[str, Any] = {"left": left, "right": right}
        data.update(self.parse_options(opts_str, line_num, line_content))
        return data

    def load(self, path: str) -> dict[str, Any]:
        if not path:
            raise ValueError("Path must be valid path name")

        try:
            self.set_path(path)
            if self._path is None:
                raise ValueError("Path must be valid path name")

            result: dict[str, Any] = {"hubs": [], "connections": []}
            known_names: set[str] = set()
            start_count = 0
            end_count = 0
            nb_drones_seen = False
            is_first_meaningful_line = True

            with open(self._path, "r") as maps:
                for line_num, raw_line in enumerate(maps, start=1):
                    line = raw_line.strip()

                    if line.startswith("#") or not line:
                        continue

                    if ":" not in line:
                        raise ParserError(
                            line_num,
                            line,
                            "missing ':' separator")

                    label, arg = line.split(":")
                    label, arg = label.strip(), arg.strip()

                    if label not in self._keys:
                        raise ParserError(
                            line_num,
                            line,
                            f"unknown label '{label}'")

                    if is_first_meaningful_line and label != "nb_drones":
                        raise ParserError(
                            line_num,
                            line,
                            "'nb_drones' must be the first line of the file"
                        )
                    is_first_meaningful_line = False

                    if label == "nb_drones":
                        if nb_drones_seen:
                            raise ParserError(
                                line_num,
                                line,
                                "'nb_drones' defined more than once")
                        if not arg.lstrip("-").isdigit():
                            raise ParserError(
                                line_num,
                                line,
                                f"nb_drones must be an integer, got '{arg}'"
                            )
                        value = int(arg)
                        if value <= 0:
                            raise ParserError(
                                line_num,
                                line,
                                f"nb_drones must be positive int, got {value}"
                            )
                        result["nb_drones"] = value
                        nb_drones_seen = True

                    elif label in ("start_hub", "end_hub", "hub"):
                        hub_data = self.parse_hub_line(arg, line_num, line)
                        name = hub_data["name"]
                        if name in known_names:
                            raise ParserError(line_num,
                                              line,
                                              f"duplicate zone name '{name}'")
                        known_names.add(name)

                        if label == "start_hub":
                            if start_count >= 1:
                                raise ParserError(
                                    line_num,
                                    line,
                                    "multiple 'start_hub' defined")
                            start_count += 1
                            result["start_hub"] = hub_data
                        elif label == "end_hub":
                            if end_count >= 1:
                                raise ParserError(line_num,
                                                  line,
                                                  "multiple 'end_hub' defined")
                            end_count += 1
                            result["end_hub"] = hub_data
                        else:
                            result["hubs"].append(hub_data)

                    elif label == "connection":
                        conn_data = self.parse_connection_line(
                            arg, line_num, line)
                        left, right = conn_data["left"], conn_data["right"]

                        if left not in known_names:
                            raise ParserError(
                                line_num,
                                line,
                                f"connection reference undefined z_'{left}'"
                            )
                        if right not in known_names:
                            raise ParserError(
                                line_num,
                                line,
                                f"connection reference undefined z_'{right}'"
                            )
                        if left == right:
                            raise ParserError(
                                line_num,
                                line,
                                f"self-loop connection '{left}-{right}'")

                        pair = frozenset((left, right))
                        is_duplicate = any(
                            frozenset((c["left"], c["right"])) == pair
                            for c in result["connections"]
                        )
                        if is_duplicate:
                            raise ParserError(
                                line_num,
                                line,
                                f"duplicate connection '{left}-{right}'"
                            )
                        result["connections"].append(conn_data)

            if not nb_drones_seen:
                raise ParserError(0, "",
                                  "'nb_drones' is missing from the file")
            if start_count != 1:
                raise ParserError(
                    0, "",
                    f"expected exactly one 'start_hub', found {start_count}")
            if end_count != 1:
                raise ParserError(
                    0, "",
                    f"expected exactly one 'end_hub', found {end_count}")

            self._result = result
            return result

        except ParserError:
            raise
        except FileNotFoundError as e:
            raise FileNotFoundError(e)
        except IsADirectoryError as e:
            raise IsADirectoryError(e)
        except ValueError as e:
            raise ValueError(e)
        except PermissionError as e:
            raise PermissionError(e)
        except Exception as e:
            raise Exception(e)
