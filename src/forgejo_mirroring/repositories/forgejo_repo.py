import time
from forgejo_mirroring.repositories.forge_api import ForgeApi
from forgejo_mirroring.config import (
    FORGEJO_DOMAIN,
    FORGEJO_TOKEN,
    PER_PAGE,
)
from forgejo_mirroring.services import Parser
from forgejo_mirroring.models import Repository, Gitforge
from forgejo_mirroring.logging import log
from .request_method import RequestMethod


class ForgejoRepo(ForgeApi):
    def __init__(self):
        super().__init__(
            self._set_headers(),
            self._set_api_url(),
            FORGEJO_TOKEN or "",
        )

    def listing(self):
        page = 1

        while True:
            response = self.request(
                "/user/repos",
                RequestMethod.GET,
                {
                    "order_by": "oldest",
                    "limit": PER_PAGE,
                    "page": page,
                },
            )
            body = self._parse_body(response)
            if not body:
                break

            for repo in body:
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
            if repository.mirrored:
                log.warning(f"Delete Forgejo `{repository.full_name}`")
                success = self.delete_repository(repository)
                if success is not True:
                    log.error(f"  Forgejo `{repository.full_name}` failed to delete")

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
                msg = f"{repository.forge.get_forge_name()} `{repository.full_name}` ready"
                if repository.archived:
                    log.info(f"{msg} (archived)")
                else:
                    log.info(msg)
                return True

            if resp.status_code in [409]:
                log.warning(
                    f"Already exists for {repository.forge.value} {repository.full_name}"
                )
                return False

        except Exception as e:
            log.error(
                f"Error migrating {repository.forge.value} {repository.full_name}: {e}"
            )

        log.error(f"Error migrating {repository.forge.value} {repository.full_name}")

        return False

    def delete_repository(self, repository: Repository) -> bool:
        resp = self.request(
            f"/repos/{repository.group}/{repository.name}",
            RequestMethod.DELETE,
        )

        return resp.status_code in [204]

    def is_exists(self, repository: Repository) -> bool:
        resp = self.request(
            f"/repos/{repository.group}/{repository.name}",
            RequestMethod.GET,
        )
        print(resp)
        print(resp.request.path_url)

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
