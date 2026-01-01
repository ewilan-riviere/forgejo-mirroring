from typing import Union, List, Tuple, Any, Mapping


class Parser:
    def __init__(self, data: Any):
        self.data = data

    def get(self, key: Union[str, List[str], Tuple[str, ...]]) -> Any:
        """Récupère une clé simple ou un chemin imbriqué sous forme de liste ou tuple."""
        if not isinstance(self.data, Mapping):
            return None

        current: Any = self.data  # type: ignore
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
