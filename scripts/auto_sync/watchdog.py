import pathlib
import subprocess
import time
from typing import Any, Dict

try:  # Optional dependency
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    yaml = None

ROOT = pathlib.Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "scripts" / "auto_sync" / "config.yaml"


def load_config() -> Dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {"watch_interval": 10, "auto_pull": True}

    try:
        if yaml is None:
            raise ImportError("PyYAML not installed")

        with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
            return yaml.safe_load(config_file) or {}
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Failed to load config: {exc}")
        return {"watch_interval": 10, "auto_pull": True}


def main() -> None:
    config = load_config()
    interval = int(config.get("watch_interval", 10))
    auto_pull_enabled = bool(config.get("auto_pull", True))

    last_hash = None

    while True:
        try:
            current = (
                subprocess.check_output("git rev-parse HEAD", shell=True)
                .decode()
                .strip()
            )

            if last_hash and current != last_hash and auto_pull_enabled:
                print("Repository changed → pulling updates")
                subprocess.run("git pull --rebase", shell=True, check=False)

            last_hash = current
        except subprocess.CalledProcessError as err:
            print(f"Watchdog unable to read git state: {err}")

        time.sleep(interval)


if __name__ == "__main__":
    main()
