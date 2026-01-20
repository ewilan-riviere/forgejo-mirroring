import platform
import subprocess
from typing import Union, List, Tuple, Any, Mapping


def alert_sound():
    """Play alert sound"""
    current_os = platform.system()

    if current_os == "Windows":
        try:
            import winsound  # pylint: disable=import-outside-toplevel

            # Note: winsound.Beep est bloquant par nature.
            # Pour Windows, on utilise PlaySound avec le flag SND_ASYNC
            winsound.PlaySound(  # type: ignore
                "SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC  # type: ignore
            )
        except ImportError:
            print("\a")

    elif current_os == "Darwin":  # macOS
        try:
            # Popen ne bloque pas le script
            subprocess.Popen(["afplay", "/System/Library/Sounds/Glass.aiff"])
        except FileNotFoundError:
            print("\a")

    elif current_os == "Linux":
        try:
            # Utilisation de Popen ici aussi
            subprocess.Popen(["canberra-gtk-play", "--id", "message-new-instant"])
        except FileNotFoundError:
            print("\x07", end="", flush=True)

    else:
        print("\a")


def extract(data: Any, key: Union[str, List[str], Tuple[str, ...]]) -> Any:
    """Retrieves a single key or a nested path as a list or tuple."""
    if not isinstance(data, Mapping):
        return None

    current: Any = data  # type: ignore
    if isinstance(key, str):
        return current.get(key)
    elif isinstance(key, (list, tuple)):  # type: ignore
        for k in key:
            if isinstance(current, Mapping) and k in current:
                current = current[k]  # type: ignore
            else:
                return None
        return current  # type: ignore
    else:
        raise TypeError("Key must be a string or a list/tuple of strings")
