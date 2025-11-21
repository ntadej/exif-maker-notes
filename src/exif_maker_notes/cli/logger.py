"""Common logging setup."""

from __future__ import annotations

from logging import DEBUG, INFO, Formatter, Logger, getLogger
from logging.handlers import RotatingFileHandler
from typing import TYPE_CHECKING

from rich import print as rprint
from rich.color import Color
from rich.logging import RichHandler
from rich.panel import Panel
from rich.style import Style
from rich.table import Table

if TYPE_CHECKING:
    from exif_maker_notes.cli.config import TyperState


def setup_logger(state: TyperState, name: str | None = None) -> Logger:
    """Prepare logger and write the log file."""
    if name and state.log_path is not None:
        file_formatter = Formatter(
            "%(asctime)s %(levelname)-8s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_path = state.log_path / f"exifmn_{name}.log"
        file_handler = RotatingFileHandler(
            file_path,
            mode="a",
            maxBytes=10 * 1024 * 1024,
            backupCount=3,
        )
        file_handler.setFormatter(file_formatter)

    stream_handler = RichHandler(
        show_path=state.debug,
        log_time_format="%Y-%m-%d %H:%M:%S",
    )

    logger = getLogger()
    if name and state.log_path is not None:
        logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    if state.debug:  # pragma: no cover
        logger.setLevel(DEBUG)
    else:
        logger.setLevel(INFO)

    return logger


def info_panel(message: str | Table, title: str = "Information") -> None:
    """Print info message in a panel."""
    rprint(
        Panel(
            message,
            title=title,
            title_align="left",
            border_style=Style(color=Color.parse("blue")),
        ),
    )


def config_table() -> Table:
    return Table.grid("Key", "Label", "Value", padding=(0, 3))


__all__ = ["Logger", "Table"]
