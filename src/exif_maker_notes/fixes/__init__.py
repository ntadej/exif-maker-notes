"""Exif Maker Notes Fixes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from exif_maker_notes.fixes.hardware import LensFix
from exif_maker_notes.fixes.timezone import TimezoneFix

if TYPE_CHECKING:
    from pathlib import Path

    from exif_maker_notes.cli.logger import Logger
    from exif_maker_notes.fixes.fix import Fix


def apply_fixes(photos: list[Path], logger: Logger, dry_run: bool = False) -> None:
    """Apply fixes to the given photos."""
    fixes: list[Fix] = [
        TimezoneFix(logger),
        LensFix(logger),
    ]

    for fix in fixes:
        fix.run(photos, dry_run=dry_run)
