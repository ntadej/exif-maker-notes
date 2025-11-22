"""Exif Maker Notes Fixes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from exif_maker_notes.fixes.hardware import LensModelFix
from exif_maker_notes.fixes.timezone import TimezoneFix
from exif_maker_notes.tool import list_metadata, set_metadata

if TYPE_CHECKING:
    from pathlib import Path

    from exif_maker_notes.cli.logger import Logger
    from exif_maker_notes.fixes.fix import Fix


def apply_fixes(photos: list[Path], logger: Logger, dry_run: bool = False) -> None:
    """Apply fixes to the given photos."""
    fixes: list[Fix] = [
        TimezoneFix(logger),
        LensModelFix(logger),
    ]

    metadata_list = list_metadata(photos)
    for photo in photos:
        metadata = metadata_list.get(photo, {})

        fixes_to_apply: dict[str, str] = {}
        for fix in fixes:
            fixes_to_apply.update(fix.apply(photo, metadata))

        set_metadata(
            photo,
            fixes_to_apply,
            logger,
            dry_run=dry_run,
        )
