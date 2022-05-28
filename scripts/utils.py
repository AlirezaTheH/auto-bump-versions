from typing import Optional, Tuple

from keepachangelog._versioning import initial_semantic_version, to_semantic
from packaging.version import Version


def _actual_version(changelog: dict) -> Tuple[Optional[str], dict]:
    versions = sorted(
        [
            (version, to_semantic(version))
            for version in changelog.keys()
            if version != 'unreleased'
        ],
        key=lambda version: Version(version[0]),
    )
    if versions:
        return versions[-1]

    return None, initial_semantic_version.copy()
