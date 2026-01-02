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

    log.skip()
    log.info(f"GitHub {len(github.repositories)} repositories")
    log.info(f"GitLab {len(gitlab.repositories)} repositories")
    log.info(f"Forgejo {len(forgejo.repositories)} repositories")
