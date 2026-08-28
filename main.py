# from infrastructure import MapModel, TxtParser
from interface import SceneManager
from infrastructure import PathParser
from configparser import ConfigParser


def main() -> None:
    config = ConfigParser()
    p_namager = PathParser()
    with open("config.ini", "r") as file:
        config.read_file(file)
    win = SceneManager("F L Y - I N G", config, p_namager)
    win.run()


if __name__ == "__main__":
    # try:
    #    main()
    # except Exception as e:
    #    print(e)
    main()
