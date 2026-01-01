import sys
from datetime import datetime
from typing import Optional
from .logger_color import LoggerColor


class Logger:
    def __init__(self, use_color: bool = True):
        self.use_color = use_color and sys.stdout.isatty()

    def _fmt(
        self,
        message: str,
        level: Optional[str] = None,
        with_dt: bool = True,
        color: Optional[LoggerColor] = None,
    ):
        base = f"{message}"

        if level:
            base = f"[{level}] {base}"

        if with_dt:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            base = f"[{ts}] {base}"

        if self.use_color and color:
            return f"{color.value}{base}{LoggerColor.RESET.value}"

        return base

    def skip(self):
        print("")

    def title(self, message: str):
        print(
            self._fmt(
                message=message,
                with_dt=False,
                color=LoggerColor.BOLD,
            )
        )

    def comment(self, message: str):
        print(
            self._fmt(
                message=message,
                with_dt=False,
                color=LoggerColor.BROWN,
            )
        )

    def info(self, message: str):
        print(
            self._fmt(
                message=message,
                level="INFO",
                color=LoggerColor.CYAN,
            )
        )

    def success(self, message: str):
        print(
            self._fmt(
                message=message,
                level="SUCCESS",
                color=LoggerColor.GREEN,
            )
        )

    def warning(self, message: str):
        print(
            self._fmt(
                message=message,
                level="WARNING",
                color=LoggerColor.YELLOW,
            ),
            file=sys.stderr,
        )

    def error(self, message: str):
        print(
            self._fmt(
                message=message,
                level="ERROR",
                color=LoggerColor.RED,
            ),
            file=sys.stderr,
        )
