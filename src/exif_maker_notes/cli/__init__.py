"""Exif Maker Notes CLI."""

from pathlib import Path
from typing import Annotated

import typer

from exif_maker_notes import __version__

from .config import TyperState
from .logger import setup_logger

application = typer.Typer(no_args_is_help=True)
state = TyperState()


def version_callback(value: bool) -> None:
    """Version callback."""
    if value:
        typer.echo(f"Exif Maker Notes, version {__version__}")
        raise typer.Exit


@application.callback()
def main(
    debug: Annotated[
        bool,
        typer.Option(
            "--debug",
            help="Run with debug printouts.",
        ),
    ] = False,
    version: Annotated[  # noqa: ARG001
        bool,
        typer.Option(
            "--version",
            help="Show version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Exif Maker Notes CLI app."""
    state.debug = debug


@application.command()
def config(
    key: Annotated[
        str,
        typer.Argument(
            help="Configuration key to set or get.",
        ),
    ] = "",
    value: Annotated[
        str,
        typer.Argument(
            help="Configuration value to set.",
        ),
    ] = "",
    file: Annotated[
        Path,
        typer.Option("-f", "--file", help="Configuration location."),
    ] = Path(),
) -> None:
    """Show or edit configuration."""
    from .config import load_configuration

    configuration = load_configuration(file)

    if not key:
        configuration.print()
    elif not value:
        typer.echo(configuration.get_key(key))
    else:
        configuration.set_key(key, value)


@application.command("list")
def list_exif(
    photos: Annotated[
        list[Path],
        typer.Argument(
            help="List of photo paths.",
        ),
    ],
) -> None:
    """List EXIF data for a list of photos."""
    logger = setup_logger(state, "list")

    import exiftool

    with exiftool.ExifToolHelper(common_args=["-G"]) as et:
        metadata = et.get_metadata(photos)
        for d in metadata:
            logger.info("Metadata for %s:", d["SourceFile"])
            for key, value in d.items():
                if key != "SourceFile":
                    logger.info("  %s: %s", key, value)
