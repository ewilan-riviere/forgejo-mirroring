# Forgejo Migrate

[![python][python-version-src]][python-version-href]

```sh
pip install dotenv requests
pip install urllib3==1.26.6
```

Create `.env`:

```sh
cp .env.example .env
```

Set `GITLAB_USER`, `GITLAB_TOKEN`, `GITLAB_ORGS`, `GITHUB_USER`, `GITHUB_TOKEN`, `GITHUB_ORGS`, `FORGEJO_INSTANCE` and `FORGEJO_TOKEN`.

Forgejo API: <https://codeberg.org/api/swagger> (or with `YOUR_OWN_INSTANCE/api/swagger`)

## Usage

Keep existing mirrors on forgejo and mirroring repositories from GitLab and GitHub (if not exists).

```sh
python forgejo-migrate
```

### Override

Delete all mirroring repositories on forgejo and mirroring repositories from GitLab and GitHub.

```sh
python forgejo-migrate --override
```

[python-version-src]: https://img.shields.io/static/v1?style=flat&label=Python&message=v3.9&color=3776AB&logo=python&logoColor=ffffff&labelColor=18181b
[python-version-href]: https://www.python.org/
