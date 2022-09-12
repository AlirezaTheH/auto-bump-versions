from typing import Optional, Union

import keepachangelog
import typer
from keepachangelog._changelog import release_version
from keepachangelog._versioning import guess_unreleased_version
from utils import _actual_version


def _release(changelog_path: str, new_version: str = None) -> str:
    changelog = keepachangelog.to_dict(changelog_path, show_unreleased=True)
    current_version, current_semantic_version = _actual_version(changelog)
    if new_version is None:
        new_version = guess_unreleased_version(
            changelog, current_semantic_version
        )
    release_version(changelog_path, current_version, new_version)
    return new_version


def _normalize_value(value: Union[str, bool]) -> str:
    if isinstance(value, str):
        return value
    elif isinstance(value, bool):
        return 'true' if value else 'false'


def set_output(name: str, value: Union[str, bool]) -> None:
    """
    Sets GitHub action output.
    """
    typer.echo(f'::set-output name={name}::{_normalize_value(value)}')


def main(new_version: Optional[str] = None) -> None:
    """
    Main script function

    Outputs:
    -------
    new-version: str
        New bumped version
    """
    new_version = _release('./CHANGELOG.md', new_version)
    set_output('new-version', new_version)


if __name__ == '__main__':
    typer.run(main)
