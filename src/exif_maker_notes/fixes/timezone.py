"""Timezone related fixes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from exif_maker_notes.fixes.fix import Fix
from exif_maker_notes.tool import list_metadata, set_metadata

if TYPE_CHECKING:
    from pathlib import Path


class TimezoneFix(Fix):
    """Timezone fix."""

    @property
    def fix_description(self) -> str:
        """Fix description."""
        return "Copy timezone information from Maker notes to the main EXIF."

    def run(self, photos: list[Path], dry_run: bool = False) -> None:
        """Run the timezone fix."""
        metadata = list_metadata(photos)
        for photo in photos:
            data = metadata.get(photo, {})
            maker_note_timezone = data.get("MakerNotes:TimeZone")
            if maker_note_timezone:
                if self.logger:
                    self.logger.info(
                        "Setting timezone for %s to %s",
                        photo,
                        maker_note_timezone,
                    )

                set_metadata(
                    photo,
                    {"EXIF:OffsetTime": maker_note_timezone},
                    self.logger,
                    dry_run=dry_run,
                )
