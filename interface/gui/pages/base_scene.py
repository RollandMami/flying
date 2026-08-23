from abc import ABC, abstractmethod
import pygame


class BaseScene(ABC):

    def __init__(self, manager) -> None:
        self.manager = manager

    @abstractmethod
    def event_handler(self, event: pygame.event.Event) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        pass