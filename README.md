# Forgejo Mirroring

[![python][python-version-src]][python-version-href]

Quickly back up your GitHub and GitLab repositories via Forgejo with mirroring.

## Environnement

Create `.env`:

```sh
cp .env.example .env
```

**For GitHub**

- `GITHUB_TOKEN`: set GitHub token, go to <https://github.com/settings/tokens> to generate it (check [which options to choose for the token](#tokens))
- `GITLAB_ORGS`: set GitHub username and organizations you want to mirror

GitHub API: <https://docs.github.com/en/rest/about-the-rest-api/about-the-rest-api>

**For GitLab**

Here domain is `gitlab.com`, of course you can replace with your own instance.

- `GITLAB_DOMAIN`: set GitLab domain, default is `gitlab.com`
- `GITLAB_TOKEN`: set GitLab token, go to <https://gitlab.com/-/user_settings/personal_access_tokens> to generate it (check [which options to choose for the token](#tokens))
- `GITLAB_ORGS`: set GitLab username and organizations you want to mirror

GitLab API: <https://docs.gitlab.com/api/rest> or [Endpoints available for GitHub App user access tokens](https://docs.github.com/en/rest/authentication/endpoints-available-for-github-app-user-access-tokens)

**For Forgejo**

Here domain is `codeberg.org`, of course you can replace with your own instance.

- `FORGEJO_DOMAIN`: set Forgejo domain, default is `codeberg.org`
- `FORGEJO_TOKEN`: set Forgejo token, go to <https://codeberg.org/user/settings/applications> to generate it (check [which options to choose for the token](#tokens))

Forgejo API: <https://codeberg.org/api/swagger> (or with `FORGEJO_INSTANCE/api/swagger`)

### Tokens

> [!TIP]
> For security reasons, choose a token with an expiration date. The goal of this project is to make mirroring very easy on all your repositories, so if your tokens have a one-year expiration date, you only need to run a command once a year.

**For GitHub : Personal access tokens (classic)**

<https://github.com/settings/tokens>

- `repo`: `repo:status`, `repo_deployment`, `public_repo`, `repo:invite`, `security_events`
- `read:org`

**For GitLab : Personal access tokens**

<https://gitlab.com/-/user_settings/personal_access_tokens>

- `read_api`

**For Forgejo : Access tokens**

<https://codeberg.org/user/settings/applications>

- `organization`: _Read_
- `repository`: _Read and write_
- `user`: _Read_

## Docker

Create container with `docker compose`:

```sh
docker compose up -d --build
```

Run application:

```sh
docker exec -it forgejo-mirroring python /app
```

## Local

### Dependencies

You have to use Python v3.14 or later, install requirements from `pip freeze > requirements.txt`

```sh
pip install -r requirements.txt
```

### Usage

Mirroring repositories from GitLab and GitHub (if not exists).

```sh
python forgejo-mirroring
```

### Delete

Delete all mirroring repositories on Forgejo, before mirroring.

```sh
python forgejo-mirroring --delete
```

### Archived

Mirroring archived repositories too.

```sh
python forgejo-mirroring --archived
```

## Endpoints used

### GitHub

**API Version**: _2022-11-28_

- [**List repositories for the authenticated user**](https://docs.github.com/en/rest/repos/repos#list-repositories-for-the-authenticated-user): _GET_ `/user/repos` (`visibility`, `affiliation`, `sort`, `direction`, `per_page`, `page`)

### GitLab

**API Version**: _18.8.0_ (`/api/v4`)

- [**List projects**](https://docs.gitlab.com/api/projects/#list-all-projects): _GET_ `/projects` (`membership`, `order_by`, `sort`, `per_page`, `page`)

### Forgejo

**API Version**: _13.0.3_ (`/api/v1`)

- [**List the repos that the authenticated user owns**](https://codeberg.org/api/swagger#/user/userCurrentListRepos): _GET_ `/user/repos` (`order_by`, `limit`, `page`)
- [**Get a repository**](https://codeberg.org/api/swagger#/repository/repoGet): _GET_ `/repos/{owner}/{repo}`
- [**Delete a repository**](https://codeberg.org/api/swagger#/repository/repoDelete): _DELETE_ `/repos/{owner}/{repo}`
- [**Migrate a remote git repository**](https://codeberg.org/api/swagger#/repository/repoMigrate): _POST_ `/repos/migrate` (`clone_addr`, `repo_name`, `auth_username`, `auth_password`, `mirror`, `private`)

[python-version-src]: https://img.shields.io/static/v1?style=flat&label=Python&message=v3.14&color=3776AB&logo=python&logoColor=ffffff&labelColor=18181b
[python-version-href]: https://www.python.org/
