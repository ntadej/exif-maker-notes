"""Hardware information related fixes."""

from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING

from exif_maker_notes.fixes.fix import Fix

if TYPE_CHECKING:
    from pathlib import Path


class LensModelFix(Fix):
    """Lens model fix."""

    @property
    def fix_description(self) -> str:
        """Fix description."""
        return "Copy lens model information from Maker notes to the main EXIF."

    def apply(self, photo: Path, metadata: dict[str, str]) -> dict[str, str]:
        """Apply the lens model fix."""
        exif_lens_make = metadata.get("EXIF:LensMake")
        exif_lens_model = metadata.get("EXIF:LensModel")
        if exif_lens_make and exif_lens_model:
            return {}

        lens = metadata.get("MakerNotes:Lens", "")
        lens_type = metadata.get("MakerNotes:LensType", "")
        lens_id = metadata.get("Composite:LensID", "")
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

        return {"EXIF:LensMake": lens_make, "EXIF:LensModel": lens_full}


class Lens35mmEquivalentFix(Fix):
    """Lens 35mm equivalent fix."""

    @property
    def fix_description(self) -> str:
        """Fix description."""
        return "Fix lens 35mm equivalent."

    def apply(self, photo: Path, metadata: dict[str, str]) -> dict[str, str]:
        """Apply the lens 35mm equivalent fix."""
        lens_id = metadata.get("Composite:LensID", "")
        if "DX" not in lens_id:
            return {}

        current_35mm_equivalent = metadata.get("EXIF:FocalLengthIn35mmFormat")
        focal_length = metadata.get("EXIF:FocalLength")
        if not focal_length:
            return {}

        focal_length_raw = float(focal_length.split(" ")[0])
        if current_35mm_equivalent:
            current_35mm_equivalent_raw = float(current_35mm_equivalent.split(" ")[0])
            if current_35mm_equivalent_raw != focal_length_raw:
                return {}

        updated_35mm_equivalent_raw = ceil(focal_length_raw * 1.5)
        updated_35mm_equivalent = f"{updated_35mm_equivalent_raw} mm"

        if self.logger:
            self.logger.info(
                "Setting lens 35mm equivalent for %s to %s (%s)",
                photo,
                updated_35mm_equivalent,
                focal_length,
            )

        return {"EXIF:FocalLengthIn35mmFormat": updated_35mm_equivalent}
