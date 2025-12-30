from src.forge.api import ForgeApi
from src.variables import (
    GITLAB_DOMAIN,
    GITLAB_TOKEN,
    GITLAB_ORGS,
    PER_PAGE,
)
from src.utils import Response, Parser
from src.models import Repository, Gitforge
from .request_method import RequestMethod


class Gitlab(ForgeApi):
    def __init__(self):
        super().__init__(
            self._set_headers(),
            self._set_api_url(),
            GITLAB_TOKEN or "",
        )

    def listing(self):
        page = 1

        while True:
            resp = self.request(
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
            response = Response(resp)

            if response.has_data is False:
                break

            if not isinstance(response.data, (list, tuple)):
                continue

            for repo in response.data:
                parser = Parser(repo)
                if parser.get(["namespace", "full_path"]) in GITLAB_ORGS:
                    full_name = f"{parser.get("path_with_namespace")}"
                    if "deletion_scheduled" not in full_name:
                        self.repositories.append(
                            Repository(
                                full_name=full_name,
                                url=parser.get("web_url"),
                                forge=Gitforge.GITLAB,
                                archived=parser.get("archived"),
                            ),
                        )
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
