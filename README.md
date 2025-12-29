# Forgejo Migrate

```sh
pip install dotenv requests
pip install urllib3==1.26.6
```

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
