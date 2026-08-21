from abc import ABC, abstractmethod
from typing import Any


class BaseParser(ABC):
    @abstractmethod
    def load(self, path: str) -> dict[str, Any]:
        ...


class TxtParser(BaseParser):

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
    def parse_options(text: str) -> dict[str, Any]:
        text = text.strip()
        if not text:
            return {}
        text = text.replace("[", "").replace("]", "")
        options: dict[str, Any] = {}
        for pair in text.split():
            if "=" not in pair:
                print(f"Bad syntax: {pair}, must include '='")
                continue
            key, value = pair.split("=", 1)
            key, value = key.strip(), value.strip()
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

    def parse_hub_line(self, arg: str) -> dict[str, Any]:
        head, opts_str = self._split_head_and_options(arg)
        tokens = head.split()
        if len(tokens) < 3:
            raise ValueError(f"Malformed hub line: '{arg}'")
        name, x, y = tokens[0], float(tokens[1]), float(tokens[2])
        if "-" in name:
            raise ValueError(f"Malformed hub line: '{arg}'")
        return {
            "name": name,
            "x": x,
            "y": y,
            "meta": self.parse_options(opts_str)
        }

    def parse_connection_line(self, arg: str) -> dict[str, Any]:
        head, opts_str = self._split_head_and_options(arg)
        if "-" not in head:
            raise ValueError(f"Malformed connection line: '{arg}'")
        left, right = head.split("-", 1)
        left, right = left.strip(), right.strip()
        data: dict[str, Any] = {"left": left, "right": right}
        data.update(self.parse_options(opts_str))
        return data

    def load(self, path: str) -> dict[str, Any]:
        if not path:
            raise ValueError("Path must be valid path name")

        try:
            self.set_path(path)
            if self._path is None:
                raise ValueError("Path must be valid path name")
            result: dict[str, Any] = {"hubs": [], "connections": []}
            with open(self._path, "r") as maps:
                for raw_line in maps:
                    line = raw_line.strip()
                    if line.startswith("#") or not line:
                        continue
                    if ":" not in line:
                        raise ValueError("Bad line format, must include ':'")
                    label, arg = line.split(":")
                    label, arg = label.strip(), arg.strip()
                    if label not in self._keys:
                        raise ValueError(f"Unknown label '{label}'")
                    if "nb" in label:
                        result["nb_drones"] = int(arg)
                    elif "start" in label:
                        result["start_hub"] = self.parse_hub_line(arg)
                    elif "end" in label:
                        result["end_hub"] = self.parse_hub_line(arg)
                    elif label == "hub":
                        result["hubs"].append(self.parse_hub_line(arg))
                    elif label == "connection":
                        data = self.parse_connection_line(arg)
                        pair = frozenset((data["left"], data["right"]))
                        is_duplicate = any(
                            frozenset((cur["left"], cur["right"])) == pair
                            for cur in result["connections"]
                        )
                        if is_duplicate:
                            print(f"Skipping duplicate/reverse connection"
                                  f"{data['left']}-{data['right']}")
                        else:
                            result["connections"].append(data)
            self._result = result
            return result
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
