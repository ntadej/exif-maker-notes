"""Exif Maker Notes common fixes code."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from exif_maker_notes.cli.logger import Logger


class Fix(ABC):
    """Fix abstract base class."""

    def __init__(self, logger: Logger | None) -> None:
        """Initialize the fix."""
        self.logger = logger

    @property
    @abstractmethod
    def fix_description(self) -> str:
        """Fix description."""

    @abstractmethod
    def run(self, photos: list[Path], dry_run: bool = False) -> None:
        """Run the fix."""
