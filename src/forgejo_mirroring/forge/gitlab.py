"""GitLab forge"""

from forgejo_mirroring.models import Repository, RequestMethod, Gitforge
from forgejo_mirroring.env import (
    GITLAB_DOMAIN,
    GITLAB_TOKEN,
    GITLAB_ORGS,
    PER_PAGE,
)
import forgejo_mirroring.utils as utils
from .forge import Forge


class ForgeGitlab(Forge):
    """GitLab forge"""

    def __init__(self):
        super().__init__(
            self._set_headers(),
            self._set_api_url(),
            GITLAB_TOKEN or "",
        )

    def listing(self):
        page = 1

        while True:
            response = self.request(
                "/projects",
                RequestMethod.GET,
                {
                    "membership": True,
                    "order_by": "created_at",
                    "sort": "asc",
                    "per_page": PER_PAGE,
                    "page": page,
                },
            )
            body = self._parse_body(response)
            if not body:
                break

            for repo in body:
                if utils.extract(repo, ["namespace", "full_path"]) in GITLAB_ORGS:
                    full_name = f"{utils.extract(repo, "path_with_namespace")}"
                    if "deletion_scheduled" not in full_name:
                        repository = Repository(
                            full_name=full_name,
                            url=utils.extract(repo, "web_url"),
                            forge=Gitforge.GITLAB,
                            archived=utils.extract(repo, "archived"),
                        )

                        self.repositories.append(repository)
            page += 1

        return self

    def _set_headers(self):
        return {
            "PRIVATE-TOKEN": f"{GITLAB_TOKEN}",
        }

    def _set_token(self):
        return GITLAB_TOKEN or ""

    def _set_api_url(self):
        return f"https://{GITLAB_DOMAIN}/api/v4"
