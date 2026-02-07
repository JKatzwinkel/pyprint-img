import io
from typing import Any, Self


class Debug:
    msgs: list[str] = []

    @classmethod
    def log(cls, msg: str) -> type[Self]:
        cls.msgs.append(msg)
        return cls

    @classmethod
    def show(cls, out: io.TextIOBase | Any) -> None:
        print('\n'.join(cls.msgs), file=out)
