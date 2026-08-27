from pathlib import Path


class PathParser:
    def __init__(self, parent: str = ".") -> None:
        self.base = parent
        self.lvl_dir_dict = {
            path.name: path for path in Path(self.base).iterdir()
            if path.is_dir()}
        self.list_files = {}

    def get_files(self, level: str) -> dict[str, Path]:
        dirs = self.lvl_dir_dict.get(level)
        if dirs is not None:
            self.list_files = {
                file.name: file for file in dirs.iterdir()
                if file.is_file()}
        return self.list_files

    def get_map_file(self, level: str, id: int) -> dict[str, Path]:
        files = self.get_files(level)
        for n, p in files.items():
            if n.startswith(f"{id:02d}_"):
                return {n: p}
        return {}
