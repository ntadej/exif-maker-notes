"""Exif Maker Notes exiftool integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

import exiftool

if TYPE_CHECKING:
    from pathlib import Path

    from exif_maker_notes.cli.logger import Logger


def list_metadata(
    photos: list[Path],
    logger: Logger | None = None,
) -> dict[Path, dict[str, str]]:
    """List EXIF metadata for a list of photos."""
    metadata_output: dict[Path, dict[str, str]] = {}
    with exiftool.ExifToolHelper(common_args=["-G"]) as et:
        metadata = et.get_metadata(photos)
        for photo, data in zip(photos, metadata, strict=True):
            if logger:
                logger.info("Metadata for %s:", data["SourceFile"])
            metadata_output[photo] = {}
            for key, value in data.items():
                if key != "SourceFile":
                    if logger:
                        logger.info("  %s: %s", key, value)
                    metadata_output[photo][key] = value
    return metadata_output


def set_metadata(
    photo: Path,
    tags: dict[str, str],
    logger: Logger | None = None,
    dry_run: bool = False,
) -> None:
    """Set EXIF metadata for a photo."""
    if logger:
        logger.info("Setting metadata for %s:", photo)
        for key, value in tags.items():
            logger.info("  %s: %s", key, value)

    if not dry_run:
        with exiftool.ExifToolHelper() as et:
            et.set_tags(photo, tags=tags, params=["-P"])
