from abc import ABC, abstractmethod


class BaseWidget(ABC):

    @abstractmethod
    def draw(self) -> None:
        ...

    @abstractmethod
    def update(self) -> None:
        ...

    @abstractmethod
    def event_handler(self) -> None:
        ...
