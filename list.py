"""List git repositories"""

from repositories import forgejo_list, gitlab_list, github_list
from repository.gitforge import Gitforge
from forge import forgejo_api

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
