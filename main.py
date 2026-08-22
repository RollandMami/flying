from infrastructure import MapModel, TxtParser


def main() -> None:
    data = TxtParser().load("maps/challenger/01_the_impossible_dream.txt")
    print(data)
    model = MapModel(**data)
    print("+"*25, "\n")
    d = model.model_dump()
    for k, v in d.items():
        print(k, ": ", v, "\n")
    print("\n\nHello from flyin!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
