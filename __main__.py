import argparse
from listing.repositories import forgejo_list, gitlab_list, github_list
from repository.gitforge import Gitforge
from forge import forgejo_api


def main():
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
    keep_archived = bool(args.archived)
    print("")

    if args.override:
        print("Delete all mirroring repositories from Forgejo...")
        forgejo_api.delete_mirrors(forgejo_list())
        print("Done!")
        print("")

    print("Mirroring repositories from GitLab...")
    forgejo_api.mirroring(gitlab_list(), Gitforge.GITLAB, keep_archived)
    print("Done!")
    print("")
    print("Mirroring repositories from GitHub...")
    forgejo_api.mirroring(github_list(), Gitforge.GITHUB, keep_archived)
    print("Done!")


if __name__ == "__main__":
    main()
