"""sync command of forgejo-mirroring"""

from typing import List
from forgejo_mirroring.args import ForgejoMirroringArgs
from forgejo_mirroring.models import Repository
from forgejo_mirroring.forge import ForgeForgejo, ForgeGithub, ForgeGitlab, Forge
from forgejo_mirroring.env import logger
import forgejo_mirroring.utils as utils


class CommandSync:
    """sync command of forgejo-mirroring"""

    def __init__(self, args: ForgejoMirroringArgs, override: bool = False):
        self._args = args
        self._forgejo = ForgeForgejo()
        self._github = ForgeGithub()
        self._gitlab = ForgeGitlab()

        self._listing_forgejo()

        if override:
            self._delete_forgejo_mirrors()
            self._listing()

            self._mirror(self._github.repositories, self._github)
            self._mirror(self._gitlab.repositories, self._gitlab)
        else:
            self._listing()

            github_missing = self._forgejo.syncing(self._github.repositories)
            gitlab_missing = self._forgejo.syncing(self._gitlab.repositories)

            logger.info("Mirroring GitHub repositories...")
            self._mirror(github_missing, self._github)
            self._mirror(gitlab_missing, self._gitlab)

            if args.pull:
                self._sync_mirrors()

        utils.alert_sound()

    def _sync_mirrors(self):
        """Sync Forgejo repositories mirrors"""
        for repo in self._forgejo.repositories:
            self._forgejo.sync_mirror(repo)

    def _listing_forgejo(self):
        """Fetch Forgejo repositories"""
        logger.info("🚀 Fetch Forgejo repositories...")
        self._forgejo.listing()

    def _listing(self):
        """Fetch repositories of GitHub and GitLab"""
        logger.info("🚀 Fetch GitHub repositories...")
        self._github.listing()
        logger.info("🚀 Fetch GitLab repositories...")
        self._gitlab.listing()

    def _mirror(self, repositories: List[Repository], forge: Forge):
        """Mirror `repositories` to Forgejo"""
        self._forgejo.mirror_repositories(
            repositories,
            forge,
            self._args.archived,
        )

    def _delete_forgejo_mirrors(self):
        """Delete mirrored repositories on Forgejo"""
        mirrors = sum(1 for repo in self._forgejo.repositories if repo.mirrored)
        logger.info("Forgejo delete %s mirrors...", mirrors)
        self._forgejo.delete_mirrors()
