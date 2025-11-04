"""Main CLI tests."""

from typer.testing import CliRunner

runner = CliRunner()


def test_help() -> None:
    """Test help."""
    from exif_maker_notes.cli import application

    result = runner.invoke(application, ["--help"], catch_exceptions=False)
    assert result.exit_code == 0


def test_version() -> None:
    """Test version."""
    from exif_maker_notes.cli import application

    result = runner.invoke(application, ["--version"], catch_exceptions=False)
    assert result.exit_code == 0


def test_list() -> None:
    """Test list."""
    from exif_maker_notes.cli import application

    result = runner.invoke(
        application,
        ["list", "tests/data/NikonD5200.jpg"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
