import importlib.metadata

__version__ = importlib.metadata.version("exif-maker-notes")


def main() -> None:
    print(f"Hello from exif-maker-notes! (version {__version__})")
