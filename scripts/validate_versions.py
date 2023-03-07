from typing import Optional, Tuple

import keepachangelog
import typer
from github import Github
from keepachangelog._versioning import guess_unreleased_version
from packaging.version import Version
from utils import _actual_version


def get_local_versions(new_version: Optional[str]) -> Tuple[Version, Version]:
    """
    Gets the local version.
    """
    changelog = keepachangelog.to_dict('CHANGELOG.md', show_unreleased=True)
    current_version, current_semantic_version = _actual_version(changelog)

    if current_version is None:
        current_version = '0.0.0'

    if new_version is None:
        new_version = guess_unreleased_version(
            changelog, current_semantic_version
        )

    return Version(current_version), Version(new_version)


def get_github_version(token: str, repository_name: str) -> Version:
    """
    Gets the latest GitHub version.
    """
    github = Github(token)
    repo = github.get_repo(repository_name)
    releases = list(repo.get_releases())
    if releases:
        return Version(releases[0].tag_name)

    return Version('0.0.0')


def main(
    github_token: str = typer.Argument(...),
    github_repository: str = typer.Argument(...),
    new_version: Optional[str] = typer.Argument(None),
) -> None:
    """
    Main script function
    """
    current_version, new_version = get_local_versions(new_version)
    github_version = get_github_version(github_token, github_repository)

    if current_version != github_version:
        typer.secho(
            'Error: Current local version does not match with GitHub latest '
            'version.',
            err=True,
            fg='red',
        )
        typer.secho(
            'Hint: Fix current version in `CHANGELOG.md` and other '
            'version files.',
            fg='blue',
        )
        typer.Exit(code=1)

    if new_version <= current_version:
        typer.secho(
            'Error: `new-version` is behind or equal with current local '
            'version',
            err=True,
            fg='red',
        )
        typer.secho(
            'Hint: Give a correct `new-version`.',
            fg='blue',
        )
        typer.Exit(code=1)

    typer.secho('Versions validated successfully.', fg='green')


if __name__ == '__main__':
    typer.run(main)
