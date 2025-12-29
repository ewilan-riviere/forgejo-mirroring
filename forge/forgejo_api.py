import time
from typing import List
import requests
from repository.project import Project
from repository.gitforge import Gitforge
from variables import (
    PER_PAGE,
    FORGEJO_API,
    FORGEJO_TOKEN,
    GITLAB_TOKEN,
    GITHUB_TOKEN,
)


def headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {FORGEJO_TOKEN}",
        "Accept": "application/json",
    }


def api() -> requests.Response:
    page = 1
    return requests.get(
        f"{FORGEJO_API}/user/repos",
        headers=headers(),
        params={
            "limit": PER_PAGE,
            "page": page,
        },
        timeout=30,
    )


def delete(owner: str, repo: str) -> requests.Response:
    return requests.delete(
        f"{FORGEJO_API}/repos/{owner}/{repo}",
        headers=headers(),
        timeout=30,
    )


def migrate(project: Project, forge: Gitforge) -> requests.Response:
    repo_name = (
        f"github_{project.name}"
        if forge == Gitforge.GITHUB
        else f"gitlab_{project.name}"
    )
    auth_password = GITHUB_TOKEN if forge == Gitforge.GITHUB else GITLAB_TOKEN

    return requests.post(
        f"{FORGEJO_API}/repos/migrate",
        headers=headers(),
        json={
            "clone_addr": project.url,
            "repo_name": repo_name,
            "auth_username": "oauth2",
            "auth_password": auth_password,
            "mirror": True,
        },
        timeout=30,
    )


def delete_mirrors(projects: list[Project]):
    for project in projects:
        if project.mirror:
            print(f"Delete {project.full_name}")
            delete(project.organization, project.name)


def mirroring(projects: List[Project], forge: Gitforge):
    for project in projects:
        try:
            resp = migrate(project, forge)

            if resp.status_code in [200, 201]:
                print(f"Done for {project.forge.value} {project.full_name}")
            elif resp.status_code in [409]:
                print(f"Already exists for {project.forge.value} {project.full_name}")
            else:
                print(
                    f"Failed for {project.full_name}: {resp.status_code} - {resp.text}"
                )
            time.sleep(1)

        except Exception as e:
            print(f"Error migrating {project.forge.value} {project.full_name}: {e}")
            time.sleep(1)
