from .config import GITLAB_DOMAIN
from .repositories import GithubRepo


def main():
    print("Forgejo Mirroring app started!")
    repo = GithubRepo()
    print(repo)
    repo = repo.listing()
    print(repo.print_repositories())
