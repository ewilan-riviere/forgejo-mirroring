from src.models.gitforge import Gitforge


class Repository:
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
        self.mirror_name = (
            f"{forge.get_mirror_name()}_{self.group}_{self.name}".lower()
        )  # gl_slink-docker

    def set_mirror(self, value: bool):
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
