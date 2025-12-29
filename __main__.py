import argparse
from repositories import forgejo_list, gitlab_list, github_list
from repository.gitforge import Gitforge
from forge import forgejo_api


def main():
    parser = argparse.ArgumentParser(
        description="Migrate repositories to Forgejo with mirroring"
    )
    parser.add_argument(
        "-o", "--override", action="store_true", help="Enable override mode"
    )

    args = parser.parse_args()

    if args.override:
        print("Enable override mode")
    else:
        print("Classic mode")
    print("")

    if args.override:
        print("Delete all mirroring repositories from Forgejo...")
        forgejo_api.delete_mirrors(forgejo_list())
        print("Done!")
        print("")

    print("Mirroring repositories from GitLab...")
    forgejo_api.mirroring(gitlab_list(), Gitforge.GITLAB)
    print("Done!")
    print("")
    print("Mirroring repositories from GitHub...")
    forgejo_api.mirroring(github_list(), Gitforge.GITHUB)
    print("Done!")


if __name__ == "__main__":
    main()
