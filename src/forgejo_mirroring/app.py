import sys
import argparse
from forgejo_mirroring.repositories import GithubRepo, GitlabRepo, ForgejoRepo, ForgeApi
from forgejo_mirroring.logging import log


def pythonCheck() -> None:
    version_min = (3, 12)
    if sys.version_info < version_min:
        sys.stderr.write(
            f"Error: Python {version_min[0]}.{version_min[1]} or later required.\n"
        )
        sys.exit(1)


def parseArguments() -> tuple[bool, bool]:
    parser = argparse.ArgumentParser(
        description="Migrate repositories to Forgejo with mirroring"
    )

    help_delete = "Delete all mirroring repositories on Forgejo, before mirroring"
    help_archived = "Mirroring archived repositories too"

    parser.add_argument(
        "-do",
        "--delete",
        action="store_true",
        help=help_delete,
    )
    parser.add_argument(
        "-a",
        "--archived",
        action="store_true",
        help=help_archived,
    )

    args = parser.parse_args()
    delete = bool(args.delete)
    archived = bool(args.archived)

    if delete:
        log.comment(f"Enable delete mode: {help_delete}")
    if archived:
        log.comment(f"Enable archived mode: {help_archived}")
    log.skip()

    return (delete, archived)


def mirror_repositories(forge: ForgeApi, keep_archived: bool = False) -> ForgejoRepo:
    forgejo = ForgejoRepo()
    for repository in forge.repositories:
        if keep_archived is not True and repository.archived:
            log.warning(
                f"Skip archived {repository.forge.value} {repository.full_name}"
            )
            continue

        forgejo.mirror_repository(repository, forge.token)

    return forgejo


def main():
    log.title("Forgejo Mirroring")
    log.skip()

    pythonCheck()
    [delete, archived] = parseArguments()

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

    if delete:
        log.skip()
        mirrors = sum(1 for repo in forgejo.repositories if repo.mirrored)
        log.info(f"Forgejo delete {mirrors} mirrors...")
        forgejo.delete_mirrors()

    log.skip()
    log.info("Forgejo mirror GitHub repositories...")
    mirror_repositories(github, archived)
    log.info("Forgejo mirror GitLab repositories...")
    mirror_repositories(gitlab, archived)
    log.skip()
