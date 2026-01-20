"""GitHub forge"""

from forgejo_mirroring.models import Repository, RequestMethod, Gitforge
from forgejo_mirroring.env import (
    PER_PAGE,
    GITHUB_TOKEN,
    GITHUB_ORGS,
)
import forgejo_mirroring.utils as utils
from .forge import Forge


class ForgeGithub(Forge):
    """GitHub forge"""

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
                if utils.extract(repo, ["owner", "login"]) in GITHUB_ORGS:
                    full_name = (
                        f"{utils.extract(repo, ['owner', 'login'])}/"
                        f"{utils.extract(repo, 'name')}"
                    )
                    repository = Repository(
                        full_name=full_name,
                        url=utils.extract(repo, "html_url"),
                        forge=Gitforge.GITHUB,
                        archived=utils.extract(repo, "archived"),
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
