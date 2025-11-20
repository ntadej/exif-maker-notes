"""Main CLI tests."""

from typer.testing import CliRunner

from exif_maker_notes.cli import application

runner = CliRunner()


def test_config_print() -> None:
    """Test print config."""
    result = runner.invoke(application, ["config"], catch_exceptions=False)
    assert result.exit_code == 0


def test_config_get() -> None:
    """Test version."""
    result = runner.invoke(
        application,
        ["config", "fixes.timezone"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert result.output.strip() == "True"


def test_config_set() -> None:
    """Test list."""
    result = runner.invoke(
        application,
        ["config", "fixes.timezone", "False"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    result = runner.invoke(
        application,
        ["config", "fixes.timezone"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert result.output.strip() == "False"

    result = runner.invoke(
        application,
        ["config", "fixes.timezone", "True"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    result = runner.invoke(
        application,
        ["config", "fixes.timezone"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert result.output.strip() == "True"
