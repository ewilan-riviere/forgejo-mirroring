from enum import Enum


class Gitforge(Enum):
    GITLAB = "gitlab"
    GITHUB = "github"
    FORGEJO = "forgejo"

    def get_mirror_name(self):
        if self is Gitforge.GITLAB:
            return "gl"
        elif self is Gitforge.GITHUB:
            return "gh"
        elif self is Gitforge.FORGEJO:
            return "fj"
        else:
            raise ValueError(f"Unsupported forge: {self}")
