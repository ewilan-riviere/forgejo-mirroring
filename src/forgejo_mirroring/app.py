from forgejo_mirroring.repositories import GithubRepo, GitlabRepo, ForgejoRepo
from forgejo_mirroring.logging import log


def main():
    log.title("Forgejo Mirroring app started!")
    log.skip()

    log.info("Parse GitHub repositories...")
    github = GithubRepo().listing()
    log.info("Parse GitLab repositories...")
    gitlab = GitlabRepo().listing()
    log.info("Parse Forgejo repositories...")
    forgejo = ForgejoRepo().listing()

    print(len(github.repositories))
    print(len(gitlab.repositories))
    print(len(forgejo.repositories))
