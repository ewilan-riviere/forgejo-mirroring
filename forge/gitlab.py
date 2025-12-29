import requests
from variables import (
    GITLAB_API,
    GITLAB_TOKEN,
    PER_PAGE,
)


def headers() -> dict[str, str]:
    return {
        "PRIVATE-TOKEN": f"{GITLAB_TOKEN}",
    }


def api() -> requests.Response:
    page = 1
    return requests.get(
        f"{GITLAB_API}/projects",
        headers=headers(),
        params={
            "membership": "true",
            "archived": "false",
            "per_page": PER_PAGE,
            "page": page,
        },
        timeout=30,
    )
