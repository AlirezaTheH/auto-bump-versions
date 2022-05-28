# Auto Bump Versions
GitHub action to automate bump version in `CHANGELOG.md`
([Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format) and
optionally bump other files' version using
[BumpVer](https://github.com/mbarkhau/bumpver), then commit and push changes.

## Usage
```yaml
name: Publish
on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  bump-versions:
    runs-on: ubuntu-latest
    steps:
      - uses: alirezatheh/auto-bump-versions@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          new-version: 1.2.3
          use-bumpver: true
```

The action assume:
- Python and pip are installed (e.g. by `actions/setup-python@v3`).

## Inputs
- `github-token`: GitHub token (required).
- `new-version`: Version to be released. If missing guess the new version using
  section names in unreleased changes of `CHANGELOG.md`
  ([Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format) (required).
- `use-bumpver`: If use `BumpVer` to bump local version in files other than
  `CHANGELOG.md`. If this is `true` your project root must contain
  `bumpver.toml` file, Defaults to `false` (optional).

## Acknowledgements
This action is inspired by
[pypi-auto-publish](https://github.com/etils-actions/pypi-auto-publish)
