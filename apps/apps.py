from infrastructure import TxtParser, MapModel


def extact_model_from_map(path: str) -> MapModel:
	data = TxtParser().load(path)
	return MapModel(**data)