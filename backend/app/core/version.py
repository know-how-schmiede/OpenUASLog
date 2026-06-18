from pathlib import Path
from runpy import run_path


def _load_version() -> str:
    current = Path(__file__).resolve()
    for parent in current.parents:
        version_file = parent / "version.py"
        if version_file.is_file() and version_file.resolve() != current:
            return str(run_path(version_file)["VERSION"])
    return "0.1.0"


APP_VERSION = _load_version()
