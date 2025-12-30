import time
from src.forge.api import ForgeApi
from src.variables import (
    FORGEJO_DOMAIN,
    FORGEJO_TOKEN,
    PER_PAGE,
)
from src.utils import Response, Parser
from src.models import Repository, Gitforge
from .request_method import RequestMethod


class Forgejo(ForgeApi):
    def __init__(self):
        super().__init__(
            self._set_headers(),
            self._set_api_url(),
            FORGEJO_TOKEN or "",
        )

    def listing(self):
        page = 1

        while True:
            resp = self.request(
                "/user/repos",
                RequestMethod.GET,
                {
                    "limit": PER_PAGE,
                    "page": page,
                },
            )
            response = Response(resp)

            if response.has_data is False:
                break

            if not isinstance(response.data, (list, tuple)):
                break

            for repo in response.data:
                parser = Parser(repo)
                repo = Repository(
                    full_name=f"{parser.get("full_name")}",
                    url=parser.get("html_url"),
                    forge=Gitforge.FORGEJO,
                    archived=parser.get("archived"),
                )

                if parser.get("mirror"):
                    repo.set_mirror(True)

                self.repositories.append(repo)
            page += 1

        return self

    def delete_mirrors(self):
        for repository in self.repositories:
            if repository.mirror:
                print(f"Delete Forgejo mirror {repository.full_name}")
                success = self.delete_repository(repository)
                if success is not True:
                    print(f"  Forgejo mirror {repository.full_name} failed to delete")

    def mirror_repository(self, repository: Repository, token: str) -> bool:
        try:
            resp = self.request(
                "/repos/migrate",
                RequestMethod.POST,
                {},
                {
                    "clone_addr": repository.url,
                    "repo_name": repository.mirror_name,
                    "auth_username": "oauth2",
                    "auth_password": token,
                    "mirror": True,
                    "private": True,
                },
            )
            time.sleep(0.5)

            if resp.status_code in [200, 201]:
                print(f"Done for {repository.forge.value} {repository.full_name}")
                return True

            if resp.status_code in [409]:
                print(
                    f"Already exists for {repository.forge.value} {repository.full_name}"
                )
                return False

        except Exception as e:
            print(
                f"Error migrating {repository.forge.value} {repository.full_name}: {e}"
            )

        print(f"Error migrating {repository.forge.value} {repository.full_name}")

        return False

    def delete_repository(self, repository: Repository) -> bool:
        resp = self.request(
            f"/repos/{repository.organization}/{repository.name}",
            RequestMethod.DELETE,
        )

        return resp.status_code in [204]

    def _set_headers(self):
        return {
            "Authorization": f"Bearer {FORGEJO_TOKEN}",
            "Accept": "application/json",
        }

    def _set_token(self):
        return FORGEJO_TOKEN or ""

    def _set_api_url(self):
        return f"https://{FORGEJO_DOMAIN}/api/v1"
