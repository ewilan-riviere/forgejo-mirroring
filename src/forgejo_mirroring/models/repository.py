"""Represents forge repository"""

from .gitforge import Gitforge


class Repository:
    """Represents forge repository"""

    def __init__(
        self, full_name: str, url: str, forge: Gitforge, archived: bool = False
    ):
        self.full_name = full_name  # kiwilan/slink-docker
        self.url = url  # https://gitlab.com/kiwilan/slink-docker
        self.forge = forge  # Gitforge.GITLAB

        splitted = full_name.split("/")
        self.group = splitted[0]  # kiwilan
        self.name = splitted[1]  # slink-docker
        self.archived = archived
        self.mirrored = False
        self.available_on_forgejo = False

        if forge != Gitforge.FORGEJO:
            self.mirror_name = (
                f"{forge.get_mirror_name()}_{self.group}_{self.name}".lower()
            )  # gl_slink-docker
        else:
            self.mirror_name = ""

    def set_mirrored(self, value: bool):
        """Set bool for `mirrored`"""
        self.mirrored = value

    def __str__(self):
        return f"""\nRepository: {self.full_name}
    - URL: {self.url}
    - Forge: {self.forge.name}
    - Group: {self.group}
    - Name: {self.name}
    - Archived? {self.archived}
    - Mirrored? {self.mirrored}
    - Mirror name: {self.mirror_name}\n"""
