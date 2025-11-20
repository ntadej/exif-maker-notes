"""Fix CLI tests."""

from typer.testing import CliRunner

from exif_maker_notes.cli import application

runner = CliRunner()


def test_fix() -> None:
    """Test fix."""
    result = runner.invoke(
        application,
        ["fix", "tests/data/NikonD5200.jpg"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
