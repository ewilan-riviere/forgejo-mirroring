from typing import Union, List, Tuple, Any
import requests


class Response:
    def __init__(self, response: requests.Response):
        self.response: requests.Response = response
        try:
            self.data: Union[dict[Any, Any], None] = self.response.json()
        except ValueError:
            self.data = None
        self.has_data = bool(self.data)

    def get_key(self, key: Union[str, List[str], Tuple[str, ...]]) -> Any:
        """Récupère une clé simple ou un chemin imbriqué sous forme de liste ou tuple."""
        if not self.has_data or not isinstance(self.data, dict):
            return None

        current: Any = self.data
        if isinstance(key, str):
            return current.get(key)
        elif isinstance(key, (list, tuple)):  # type: ignore
            for k in key:
                if isinstance(current, dict) and k in current:
                    current = current[k]  # type: ignore
                else:
                    return None
            return current  # type: ignore
        else:
            raise TypeError("Key must be a string or a list/tuple of strings")

    def printing(self) -> None:
        print(self.data)
