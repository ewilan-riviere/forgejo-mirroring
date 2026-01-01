import sys
from datetime import datetime
from typing import Optional
from .logger_color import LoggerColor


class Logger:
    def __init__(self, use_color: bool = True):
        self.use_color = use_color and sys.stdout.isatty()

    def _fmt(self, level: str, msg: str, color: Optional[LoggerColor] = None) -> str:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        base = f"[{ts}] [{level}] {msg}"

        if self.use_color and color:
            return f"{color.value}{base}{LoggerColor.RESET.value}"

        return base

    def info(self, msg: str):
        print(self._fmt("INFO", msg, LoggerColor.CYAN))

    def success(self, msg: str):
        print(self._fmt("OK", msg, LoggerColor.GREEN))

    def warning(self, msg: str):
        print(self._fmt("WARN", msg, LoggerColor.YELLOW), file=sys.stderr)

    def error(self, msg: str):
        print(self._fmt("ERROR", msg, LoggerColor.RED), file=sys.stderr)
