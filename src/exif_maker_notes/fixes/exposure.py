"""Exposure related fixes."""

from __future__ import annotations

import csv
from typing import TYPE_CHECKING

from exif_maker_notes.fixes.fix import Fix

if TYPE_CHECKING:
    from pathlib import Path

    from exif_maker_notes.cli.logger import Logger


class ExposureCompensationFix(Fix):
    """Exposure compensation fix."""

    def __init__(self, logger: Logger | None, config_path: Path) -> None:
        """Initialize the exposure compensation fix."""
        if not config_path.exists() or not config_path.is_file():
            error = f"Exposure compensation configuration file not found: {config_path}"
            raise FileNotFoundError(error)

        super().__init__(logger)
        self.config_path = config_path

        with config_path.open() as f:
            reader = csv.reader(f)
            self.exposure_compensation_map = {row[0]: float(row[1]) for row in reader}

    @property
    def fix_description(self) -> str:
        """Fix description."""
        return "Set exposure compensation based on postprocessing done."

    def apply(self, photo: Path, metadata: dict[str, str]) -> dict[str, str]:
        """Apply the exposure compensation fix."""
        if photo.name not in self.exposure_compensation_map:
            return {}

        exif_exposure_compensation = float(metadata.get("EXIF:ExposureCompensation", 0))
        updated_exposure_compensation = self.exposure_compensation_map[photo.name]
        if abs(updated_exposure_compensation - exif_exposure_compensation) < 1e-5:  # noqa: PLR2004
            return {}

        if self.logger:
            self.logger.info(
                "Setting exposure compensation for %s to %s",
                photo,
                updated_exposure_compensation,
            )

        return {"EXIF:ExposureCompensation": str(updated_exposure_compensation)}
