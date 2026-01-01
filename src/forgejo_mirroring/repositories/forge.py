from abc import ABC, abstractmethod
from typing import List, Self
from urllib.parse import urlencode, quote
import requests
from forgejo_mirroring.models import Repository
from .request_method import RequestMethod


class ForgeApi(ABC):
    TIMEOUT: int = 30

    def __init__(self, headers: dict[str, str], api_url: str, token: str):
        self._headers = headers
        self._api_url = api_url
        self.token = token
        self.repositories: List[Repository] = []

    def request(
        self,
        endpoint: str,
        method: RequestMethod,
        params: dict[str, str | bool | int] | None = None,
        body: dict[str, str | bool | int] | None = None,
    ):
        url = f"{self._api_url}{endpoint}"

        match method:
            case RequestMethod.GET:
                return requests.get(
                    url,
                    headers=self._headers,
                    params=params,
                    timeout=self.TIMEOUT,
                )
            case RequestMethod.POST:
                return requests.post(
                    url,
                    headers=self._headers,
                    params=params,
                    json=body,
                    timeout=self.TIMEOUT,
                )
            case RequestMethod.PATCH:
                return requests.patch(
                    url,
                    headers=self._headers,
                    params=params,
                    json=body,
                    timeout=self.TIMEOUT,
                )
            case RequestMethod.PUT:
                return requests.put(
                    url,
                    headers=self._headers,
                    params=params,
                    json=body,
                    timeout=self.TIMEOUT,
                )
            case RequestMethod.DELETE:
                return requests.delete(
                    url,
                    headers=self._headers,
                    params=params,
                    timeout=self.TIMEOUT,
                )
            case _:
                raise ValueError(f"Méthode non supportée: {method}")

    def get_full_url(
        self, url: str, params: dict[str, str | bool | int] | None = None
    ) -> str:
        query_str = ""
        if params:
            str_params = {k: str(v) for k, v in params.items()}
            query_str = urlencode(str_params, quote_via=quote, safe=",")

        return f"{url}?{query_str}" if query_str else url

    def print_repositories(self):
        i = 1
        print(len(self.repositories))
        for repo in self.repositories:
            msg = f"{i}. {repo.full_name}"
            if repo.archived:
                msg = f"{msg} (archived)"
            print(msg)
            i = i + 1

    def __str__(self):
        return f"""\nAPI URL: {self._api_url}\n"""

    @abstractmethod
    def listing(self) -> Self:
        """Forge API request"""

    @abstractmethod
    def _set_headers(self) -> dict[str, str]:
        """Forge API headers"""

    @abstractmethod
    def _set_token(self) -> str:
        """Forge API token"""

    @abstractmethod
    def _set_api_url(self) -> str:
        """Forge API URL"""
