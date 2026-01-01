# """Get variables from .env"""

import os
from dotenv import load_dotenv

load_dotenv()

# # GitLab
GITLAB_DOMAIN = os.environ.get("GITLAB_DOMAIN")
GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN")
GITLAB_ORGS = os.environ.get("GITLAB_ORGS")

# # GitHub
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_ORGS = os.environ.get("GITHUB_ORGS")

# # Forgejo
FORGEJO_DOMAIN = os.environ.get("FORGEJO_DOMAIN")
FORGEJO_TOKEN = os.environ.get("FORGEJO_TOKEN")

PER_PAGE = int(os.environ.get("PER_PAGE", 50))
