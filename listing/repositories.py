from typing import List
import requests
from variables import (
    GITLAB_API,
    GITLAB_TOKEN,
    PER_PAGE,
    GITLAB_ORGS,
    GITHUB_API,
    GITHUB_TOKEN,
    GITHUB_ORGS,
    FORGEJO_API,
    FORGEJO_TOKEN,
)
from repository.project import Project
from repository.gitforge import Gitforge


def forgejo_list() -> List[Project]:
    page = 1
    projects: List[Project] = []

    while True:
        resp = requests.get(
            f"{FORGEJO_API}/user/repos",
            headers={
                "Authorization": f"Bearer {FORGEJO_TOKEN}",
                "Accept": "application/json",
            },
            params={
                "limit": PER_PAGE,
                "page": page,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break

        for rep in data:
            repo = Project(
                full_name=rep["full_name"],
                url=rep["html_url"],
                forge=Gitforge.FORGEJO,
            )
            if rep["mirror"]:
                repo.set_mirror(True)

            projects.append(repo)
        page += 1
    return projects


def github_list() -> List[Project]:
    page = 1
    projects: List[Project] = []

    while True:
        resp = requests.get(
            f"{GITHUB_API}/user/repos",
            headers={
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json",
            },
            params={
                "visibility": "all",
                "affiliation": "owner,collaborator,organization_member",
                "per_page": PER_PAGE,
                "page": page,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break

        for rep in data:
            if rep["owner"]["login"] in GITHUB_ORGS:
                repo = Project(
                    full_name=rep["owner"]["login"] + "/" + rep["name"],
                    url=rep["html_url"],
                    forge=Gitforge.GITHUB,
                    archived=rep["archived"],
                )
                if not rep["archived"]:
                    projects.append(repo)
        page += 1
    return projects


def gitlab_list() -> List[Project]:
    page = 1
    projects: List[Project] = []

    while True:
        resp = requests.get(
            f"{GITLAB_API}/projects",
            headers={
                "PRIVATE-TOKEN": GITLAB_TOKEN,
            },
            params={
                "membership": "true",
                "per_page": PER_PAGE,
                "page": page,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break

        for rep in data:
            if rep["namespace"]["full_path"] in GITLAB_ORGS:
                repo = Project(
                    full_name=rep["path_with_namespace"],
                    url=rep["web_url"],
                    forge=Gitforge.GITLAB,
                    archived=rep["archived"],
                )
                projects.append(repo)
        page += 1
    return projects


def print_projects(repos: List[Project]) -> None:
    for repo in repos:
        print(repo)

    if len(repos) == 0:
        print("No repositories found")
