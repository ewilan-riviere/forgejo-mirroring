from repository.gitforge import Gitforge


class Project:
    """
    Classe représentant un projet GitLab ou GitHub.
    """

    def __init__(
        self, full_name: str, url: str, forge: Gitforge, archived: bool = False
    ):
        """
        Repository
        """
        self.full_name = full_name  # kiwilan/slink-docker
        self.url = url  # https://gitlab.com/kiwilan/slink-docker
        self.forge = forge  # Gitforge.GITLAB

        splitted = full_name.split("/")
        self.organization = splitted[0]  # kiwilan
        self.name = splitted[1]  # slink-docker
        self.archived = archived
        self.mirror = False

    def set_mirror(self, value: bool):
        self.mirror = value

    def __str__(self):
        """Représentation lisible de l'objet pour print()"""
        return f"{self.organization}/{self.name} from {self.url} on {self.forge.value}"
