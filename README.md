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

For GitLab

Here domain is `gitlab.com`, of course you can replace with your own instance.

- `GITLAB_DOMAIN`: set GitLab domain, default is `gitlab.com`
- `GITLAB_TOKEN`: set GitLab token, go to <https://gitlab.com/-/user_settings/personal_access_tokens> to generate it
- `GITLAB_ORGS`: set GitLab username and organization you want to mirror

For GitHub

- `GITHUB_TOKEN`: set GitHub token, go to <https://github.com/settings/tokens> to generate it
- `GITLAB_ORGS`: set GitHub username and organization you want to mirror

For Forgejo

Here domain is `codeberg.org`, of course you can replace with your own instance.

- `FORGEJO_DOMAIN`: set Forgejo domain, default is `codeberg.org`
- `FORGEJO_TOKEN`: set Forgejo token, go to <https://codeberg.org/user/settings/applications> to generate it

Forgejo API: <https://codeberg.org/api/swagger> (or with `FORGEJO_INSTANCE/api/swagger`)

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

### Archived

Mirroring archived repositories (default mode don't mirror it).

```sh
python forgejo-migrate --archived
```

[python-version-src]: https://img.shields.io/static/v1?style=flat&label=Python&message=v3.14&color=3776AB&logo=python&logoColor=ffffff&labelColor=18181b
[python-version-href]: https://www.python.org/
