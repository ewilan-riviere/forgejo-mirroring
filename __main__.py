import argparse
import sys
from src.forge import Gitlab, Github, Forgejo, ForgeApi


def listing_forgejo(delete: bool = False) -> Forgejo:
    print("")
    print("Listing Forgejo repositories...")
    print("")
    forgejo = Forgejo().listing()
    if delete:
        print("Deleting Forgejo mirrors repositories...")
        print("")
        forgejo.delete_mirrors()
        print("")

    return forgejo


def listing_github() -> ForgeApi:
    print("")
    print("Parse GitHub repositories...")
    print("")
    github = Github().listing()

    return github


def listing_gitlab() -> ForgeApi:
    print("")
    print("Parse GitLab repositories...")
    print("")
    gitlab = Gitlab().listing()

    return gitlab


def mirror(forge: ForgeApi, keep_archived: bool = False) -> Forgejo:
    forgejo = Forgejo()
    for repository in forge.repositories:
        if keep_archived is not True and repository.archived:
            print(f"Skip archived {repository.forge.value} {repository.full_name}")
            continue

        forgejo.mirror_repository(repository, forge.token)

    return forgejo


def main():
    print("forgejo-migrate")

    version_min = (3, 14)
    if sys.version_info < version_min:
        sys.stderr.write(
            f"Error: Python {version_min[0]}.{version_min[1]} or later required.\n"
        )
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Migrate repositories to Forgejo with mirroring"
    )
    parser.add_argument(
        "-o", "--override", action="store_true", help="Enable override mode"
    )
    parser.add_argument(
        "-a", "--archived", action="store_true", help="Mirror archived repositories too"
    )

    args = parser.parse_args()

    if args.override:
        print("Enable override mode")
    if args.archived:
        print("Enable archived mode")
    override = bool(args.override)
    keep_archived = bool(args.archived)
    print("")

    listing_forgejo(override)

    github = listing_github()
    mirror(github, keep_archived)

    gitlab = listing_gitlab()
    mirror(gitlab, keep_archived)


if __name__ == "__main__":
    main()
