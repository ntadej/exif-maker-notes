"""Configuration utilities."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

import tomli_w
from platformdirs import user_config_dir

from .logger import Table, config_table, info_panel


def strtobool(val: str) -> bool:
    """Convert a string representation of truth to True or False.

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    if val in ("n", "no", "f", "false", "off", "0"):
        return False
    error = f"invalid truth value {val!r}"
    raise ValueError(error)


class TyperState:
    """Execution configuration state."""

    def __init__(self) -> None:
        """Initialize configuration state."""
        self.debug: bool = False
        self.log_path: Path | None = None


class Configuration:
    """Main configuration."""

    def __init__(self, location: Path) -> None:
        """Initialize main configuration."""
        self.location: Path = location

        if not location.exists():
            config = {}
        else:
            with location.open(mode="rb") as f:
                config = tomllib.load(f)

        self.fixes = FixesConfiguration(config.get("fixes", {}))

    def get_key(self, key: str) -> Any:  # noqa: ANN401
        """Get configuration key."""
        split_key = key.split(".")
        if len(split_key) != 2:  # noqa: PLR2004
            error = f"Invalid configuration key: {key}"
            raise KeyError(error)

        config_object = self.to_object()
        if split_key[0] not in config_object:
            error = f"Invalid configuration key: {key}"
            raise KeyError(error)

        if split_key[1] not in config_object[split_key[0]]:
            error = f"Invalid configuration key: {key}"
            raise KeyError(error)

        return config_object[split_key[0]][split_key[1]]

    def set_key(self, key: str, value: str) -> None:
        """Set configuration key."""
        split_key = key.split(".")
        if len(split_key) != 2:  # noqa: PLR2004
            error = f"Invalid configuration key: {key}"
            raise KeyError(error)

        config_object = self.to_object()
        if split_key[0] not in config_object:
            error = f"Invalid configuration key: {key}"
            raise KeyError(error)

        if split_key[1] not in config_object[split_key[0]]:
            error = f"Invalid configuration key: {key}"
            raise KeyError(error)

        if isinstance(config_object[split_key[0]][split_key[1]], bool):
            config_object[split_key[0]][split_key[1]] = strtobool(value)
        else:
            config_object[split_key[0]][split_key[1]] = value

        self.write(self.location, config_object)

    def to_object(self) -> dict[str, Any]:
        """Convert configuration to object."""
        return {
            "fixes": self.fixes.to_object(),
        }

    def to_table(self) -> Table:
        """Convert configuration to table."""
        table = config_table()
        table.add_row("Configuration location", str(self.location))
        return table

    def print(self) -> None:
        """Print configuration."""
        info_panel(self.to_table(), title="Main Configuration")
        info_panel(self.fixes.to_table(), title="Fixes Configuration")

    def write(self, output_file: Path, config_object: dict[str, Any]) -> None:
        """Write configuration to file."""
        if not output_file.parent.exists():
            output_file.parent.mkdir(parents=True)
        with output_file.open(mode="wb") as f:
            tomli_w.dump(config_object, f)


def load_configuration(file: Path) -> Configuration:
    """Load configuration from default location."""
    if file.is_file() and file.exists():
        return Configuration(location=file)

    config_dir = Path(user_config_dir("exifmn"))
    config_path = config_dir / "config.toml"
    return Configuration(location=config_path)


class FixesConfiguration:
    """Fixes configuration."""

    def __init__(self, config: dict[str, bool]) -> None:
        """Initialize fixes configuration."""
        self.timezone = config.get("timezone", True)

    def to_object(self) -> dict[str, Any]:
        """Convert fixes configuration to object."""
        return {
            "timezone": self.timezone,
        }

    def to_table(self) -> Table:
        """Convert configuration to table."""
        table = config_table()

        table.add_row("fixes.timezone", "Timezone", str(self.timezone))

        return table
