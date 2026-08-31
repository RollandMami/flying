from typing import Optional
from .RadioButton import RadioButton


class RadioGroup:

    def __init__(self) -> None:
        self.radios: list[RadioButton] = []
        self._active: Optional[RadioButton] = None

    def add_radio(self, btn: RadioButton) -> None:
        if btn not in self.radios:
            self.radios.append(btn)
            original_call = btn.callable

            def on_click() -> None:
                self.select(btn)
                if original_call is not None:
                    original_call()

            btn.callable = on_click
        elif any(r.value == btn.value for r in self.radios):
            raise ValueError("Duplicate object...")

    def select(self, btn: RadioButton) -> None:
        self._active = btn
        self.sync_states()

    def sync_states(self) -> None:
        for rd in self.radios:
            rd.is_selected = (rd is self._active)

    def event_handler(self) -> None:
        for rd in self.radios:
            rd.event_handler()

    def set_active(self, value: str) -> None:
        for rdo in self.radios:
            if value == rdo.value:
                self.select(rdo)
                return

    @property
    def value(self) -> str | None:
        if self._active is not None:
            return self._active.value
        return None

    @property
    def active_button(self) -> Optional[RadioButton]:
        return self._active
