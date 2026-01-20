"""Represents forge enum"""

from enum import Enum


class Gitforge(Enum):
    """Represents forge enum"""

    GITLAB = "gitlab"
    GITHUB = "github"
    FORGEJO = "forgejo"

    def get_mirror_name(self):
        """Get forge shortcut"""
        if self is Gitforge.GITLAB:
            return "gl"
        elif self is Gitforge.GITHUB:
            return "gh"
        elif self is Gitforge.FORGEJO:
            return "fj"
        else:
            raise ValueError(f"Unsupported forge: {self}")

    def get_forge_name(self):
        """Get forge label"""
        if self is Gitforge.GITLAB:
            return "GitLab"
        elif self is Gitforge.GITHUB:
            return "GitHub"
        elif self is Gitforge.FORGEJO:
            return "Forgejo"
        else:
            raise ValueError(f"Unsupported forge: {self}")
