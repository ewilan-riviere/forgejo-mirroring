from src.forge.api import ForgeApi
from src.variables import (
    GITHUB_TOKEN,
    GITHUB_ORGS,
    PER_PAGE,
)
from src.utils import Response, Parser
from src.models import Repository, Gitforge
from .request_method import RequestMethod


class Github(ForgeApi):
    def __init__(self):
        super().__init__(
            self._set_headers(),
            self._set_api_url(),
            GITHUB_TOKEN or "",
        )

    def listing(self):
        page = 1

        while True:
            resp = self.request(
                "/user/repos",
                RequestMethod.GET,
                {
                    "visibility": "all",
                    "affiliation": "owner,collaborator,organization_member",
                    "per_page": PER_PAGE,
                    "page": page,
                },
            )
            response = Response(resp)

            if response.has_data is False:
                break

            if not isinstance(response.data, (list, tuple)):
                continue

            for repo in response.data:
                parser = Parser(repo)
                if parser.get(["owner", "login"]) in GITHUB_ORGS:
                    self.repositories.append(
                        Repository(
                            full_name=f"{parser.get(["owner", "login"])}/{parser.get("name")}",
                            url=parser.get("html_url"),
                            forge=Gitforge.GITHUB,
                            archived=parser.get("archived"),
                        ),
                    )
            page += 1

        return self

    def _set_headers(self):
        return {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
        }

    def _set_token(self):
        return GITHUB_TOKEN or ""

    def _set_api_url(self):
        return "https://api.github.com"
