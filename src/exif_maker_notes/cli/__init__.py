"""Exif Maker Notes CLI."""

from pathlib import Path
from typing import Annotated

import typer

from exif_maker_notes import __version__
from exif_maker_notes.cli.config import TyperState
from exif_maker_notes.cli.logger import setup_logger

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
    from exif_maker_notes.cli.config import load_configuration

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

    from exif_maker_notes.tool import list_metadata

    list_metadata(photos, logger)


@application.command()
def fix(
    photos: Annotated[
        list[Path],
        typer.Argument(
            help="List of photo paths.",
        ),
    ],
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Run the fixes without making any changes.",
        ),
    ] = False,
    exposure: Annotated[
        Path,
        typer.Option(
            "--exposure",
            help="Path to exposure correction configuration file.",
        ),
    ] = Path(),
    strict: Annotated[
        bool,
        typer.Option(
            "--strict",
            help="Strict mode: CSV files need to match photos exactly.",
        ),
    ] = False,
) -> None:
    """Apply fixes to EXIF data for a list of photos."""
    logger = setup_logger(state, "fix")

    from exif_maker_notes.fixes import apply_fixes

    apply_fixes(
        photos,
        logger,
        dry_run=dry_run,
        exposure_config=exposure,
        strict=strict,
    )


@application.command()
def restore(
    photos: Annotated[
        list[Path],
        typer.Argument(
            help="List of photo paths.",
        ),
    ],
) -> None:
    """Restore original photos."""
    logger = setup_logger(state, "restore")

    from exif_maker_notes.tool import restore

    for photo in photos:
        if photo.name.endswith("_original"):
            continue
        restore(photo, logger)
