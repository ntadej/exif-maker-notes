"""Hardware information related fixes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from exif_maker_notes.fixes.fix import Fix
from exif_maker_notes.tool import list_metadata, set_metadata

if TYPE_CHECKING:
    from pathlib import Path


class LensFix(Fix):
    """Lens fix."""

    @property
    def fix_description(self) -> str:
        """Fix description."""
        return "Copy lens information from Maker notes to the main EXIF."

    def run(self, photos: list[Path], dry_run: bool = False) -> None:
        """Run the lens fix."""
        metadata = list_metadata(photos)
        for photo in photos:
            data = metadata.get(photo, {})
            lens = data.get("MakerNotes:Lens", "")
            lens_type = data.get("MakerNotes:LensType", "")
            lens_id = data.get("Composite:LensID", "")
            # combine lens information
            if lens_type.startswith("G"):
                lens_full = f"{lens}{lens_type}"
            else:
                lens_full = f"{lens} {lens_type}"

            if "Nikkor" in lens_id:
                lens_make = "Nikon Corporation"
                lens_full = f"Nikkor {lens_full}"
            else:
                lens_make = ""

            if self.logger:
                self.logger.info(
                    "Setting lens for %s to %s (%s)",
                    photo,
                    lens_full,
                    lens_make,
                )

            set_metadata(
                photo,
                {"EXIF:LensMake": lens_make, "EXIF:LensModel": lens_full},
                self.logger,
                dry_run=dry_run,
            )
