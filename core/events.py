from collections import defaultdict
from typing import Callable, Any


class EventBus:
    """Глобальная шина событий (Publish-Subscribe) для развязки логики, звука и VFX."""

    def __init__(self):
        self._listeners: dict[str, list[Callable[..., None]]] = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callable[..., None]) -> None:
        if callback not in self._listeners[event_name]:
            self._listeners[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable[..., None]) -> None:
        if callback in self._listeners[event_name]:
            self._listeners[event_name].remove(callback)

    def emit(self, event_name: str, **payload: Any) -> None:
        for callback in list(self._listeners.get(event_name, ())):
            callback(**payload)

    def clear(self) -> None:
        self._listeners.clear()


# Единый экземпляр шины событий на весь проект
bus = EventBus()
