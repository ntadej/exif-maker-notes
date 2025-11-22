"""Timezone related fixes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from exif_maker_notes.fixes.fix import Fix

if TYPE_CHECKING:
    from pathlib import Path


class TimezoneFix(Fix):
    """Timezone fix."""

    @property
    def fix_description(self) -> str:
        """Fix description."""
        return "Copy timezone information from Maker notes to the main EXIF."

    def apply(self, photo: Path, metadata: dict[str, str]) -> dict[str, str]:
        """Apply the timezone fix."""
        exif_timezone = metadata.get("EXIF:OffsetTime")
        if exif_timezone:
            return {}

        maker_note_timezone = metadata.get("MakerNotes:TimeZone")
        if not maker_note_timezone:
            return {}

        if self.logger:
            self.logger.info(
                "Setting timezone for %s to %s",
                photo,
                maker_note_timezone,
            )

        return {"EXIF:OffsetTime": maker_note_timezone}
