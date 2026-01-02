from forgejo_mirroring.config import (
    PER_PAGE,
    GITHUB_TOKEN,
    GITHUB_ORGS,
)
from forgejo_mirroring.services import Parser
from forgejo_mirroring.models import Gitforge, Repository
from .forge_api import ForgeApi
from .request_method import RequestMethod


class GithubRepo(ForgeApi):
    def __init__(self):
        super().__init__(
            self._set_headers(),
            self._set_api_url(),
            GITHUB_TOKEN or "",
        )

    def listing(self):
        page = 1

        while True:
            response = self.request(
                "/user/repos",
                RequestMethod.GET,
                {
                    "visibility": "all",
                    "affiliation": "owner,collaborator,organization_member",
                    "sort": "oldest",
                    "direction": "asc",
                    "per_page": PER_PAGE,
                    "page": page,
                },
            )
            body = self._parse_body(response)
            if not body:
                break

            for repo in body:
                parser = Parser(repo)
                if parser.get(["owner", "login"]) in GITHUB_ORGS:
                    repository = Repository(
                        full_name=f"{parser.get(["owner", "login"])}/{parser.get("name")}",
                        url=parser.get("html_url"),
                        forge=Gitforge.GITHUB,
                        archived=parser.get("archived"),
                    )

                    if repository:
                        self.repositories.append(repository)
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
