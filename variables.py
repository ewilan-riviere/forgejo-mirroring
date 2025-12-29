"""List git repositories"""

import os
from dotenv import load_dotenv

load_dotenv()

# Variables communes
PER_PAGE = int(os.environ.get("PER_PAGE", 50))

# GitLab
GITLAB_API = os.environ.get("GITLAB_API")
GITLAB_USER = os.environ.get("GITLAB_USER")
GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN")
GITLAB_ORGS = os.environ.get("GITLAB_ORGS")

# GitHub
GITHUB_API = os.environ.get("GITHUB_API")
GITHUB_USER = os.environ.get("GITHUB_USER")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_ORGS = os.environ.get("GITHUB_ORGS")

# Forgejo
FORGEJO_API = os.environ.get("FORGEJO_API")
FORGEJO_TOKEN = os.environ.get("FORGEJO_TOKEN")
