"""CLI args for forgejo-mirroring"""

from argparse import ArgumentParser, Namespace


class ForgejoMirroringArgs:
    """CLI args for forgejo-mirroring"""

    def __init__(self, parser: ArgumentParser):
        subparsers = parser.add_subparsers(dest="command", required=True)

        # Sync
        m_sync = subparsers.add_parser(
            "sync", help="Sync GitHub and GitLab repositories with Forgejo"
        )
        m_sync.add_argument(
            "-a",
            "--archived",
            action="store_true",
            help="Create mirrors for archived repositories too.",
        )
        m_sync.add_argument(
            "-p",
            "--pull",
            action="store_true",
            help="Pull changements from mirrored repository.",
        )

        # Override
        m_override = subparsers.add_parser(
            "override",
            help=(
                "Erase Forgejo mirrored repositories to create new mirrors "
                "of GitHub and GitLab repositories with Forgejo"
            ),
        )
        m_override.add_argument(
            "-a",
            "--archived",
            action="store_true",
            help="Create mirrors for archived repositories too.",
        )

        args: Namespace = parser.parse_args()
        self.command: str = args.command

        self.archived: bool = getattr(args, "archived", False)
        self.pull: bool = getattr(args, "pull", False)

        print("self.archived", self.archived)
        print("self.pull", self.pull)
