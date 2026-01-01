import argparse
import sys
from src.forge import Gitlab, Github, Forgejo, ForgeApi
from logger_utils import log


def listing_forgejo(delete: bool = False) -> Forgejo:
    log.skip()
    log.info("Listing Forgejo repositories...")
    log.skip()
    forgejo = Forgejo().listing()
    if delete:
        log.warning("Deleting Forgejo mirrors repositories...")
        log.skip()
        forgejo.delete_mirrors()
        log.skip()

    return forgejo


def listing_github() -> ForgeApi:
    log.skip()
    log.info("Parse GitHub repositories...")
    log.skip()
    github = Github().listing()

    return github


def listing_gitlab() -> ForgeApi:
    log.skip()
    log.info("Parse GitLab repositories...")
    log.skip()
    gitlab = Gitlab().listing()

    return gitlab


def mirror(forge: ForgeApi, keep_archived: bool = False) -> Forgejo:
    forgejo = Forgejo()
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

    version_min = (3, 14)
    if sys.version_info < version_min:
        sys.stderr.write(
            f"Error: Python {version_min[0]}.{version_min[1]} or later required.\n"
        )
        sys.exit(1)

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

    listing_forgejo(delete)

    github = listing_github()
    mirror(github, archived)

    gitlab = listing_gitlab()
    mirror(gitlab, archived)
    log.skip()


if __name__ == "__main__":
    main()
