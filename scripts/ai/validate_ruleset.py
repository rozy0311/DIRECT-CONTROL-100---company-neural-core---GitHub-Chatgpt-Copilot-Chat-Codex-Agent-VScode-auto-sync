import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
RULESET = ROOT / "ai" / "ai_ruleset.yaml"


def main() -> None:
    if not RULESET.exists():
        print("No ai_ruleset.yaml found; skipping validation.")
        return

    try:
        import yaml  # type: ignore
    except ModuleNotFoundError:  # pragma: no cover
        print("PyYAML not installed; unable to parse ruleset.")
        return

    with RULESET.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    rules = data.get("rules", [])
    if not isinstance(rules, list):
        raise SystemExit("Ruleset must contain a list under 'rules'")

    print(f"Validated {len(rules)} rules in ai_ruleset.yaml")


if __name__ == "__main__":
    main()
