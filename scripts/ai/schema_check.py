import pathlib

try:
    from jsonschema import Draft7Validator  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    Draft7Validator = None

ROOT = pathlib.Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"

SCHEMA = {
    "type": "object",
    "properties": {
        "module": {"type": "string"},
        "owner": {"type": "string"},
        "version": {"type": "string"},
    },
    "required": ["module", "owner"],
}


def validate_config(path: pathlib.Path) -> None:
    if Draft7Validator is None:
        raise SystemExit("jsonschema not installed; cannot validate configs")

    try:
        import yaml  # type: ignore
    except ModuleNotFoundError:  # pragma: no cover
        raise SystemExit("PyYAML not installed; cannot validate configs") from None

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    validator = Draft7Validator(SCHEMA)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

    if errors:
        for error in errors:
            print(f"Schema violation in {path.name}: {error.message}")
        raise SystemExit(1)


def main() -> None:
    if not CONFIG_DIR.exists():
        print("Config directory missing; skipping schema check")
        return

    targets = sorted(CONFIG_DIR.glob("*.yaml"))
    if not targets:
        print("No config/*.yaml files found; nothing to validate")
        return

    for config_file in targets:
        validate_config(config_file)

    print(f"Validated {len(targets)} config files against governance schema")


if __name__ == "__main__":
    main()
