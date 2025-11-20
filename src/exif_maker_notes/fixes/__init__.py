"""Exif Maker Notes Fixes."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from exif_maker_notes.cli.logger import Logger
    from exif_maker_notes.fixes.fix import Fix


def apply_fixes(photos: list[Path], logger: Logger) -> None:
    """Apply fixes to the given photos."""
    from .timezone import TimezoneFix

    fixes: list[Fix] = [
        TimezoneFix(logger),
    ]

    for fix in fixes:
        fix.run(photos)
