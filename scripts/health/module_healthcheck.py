import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
BUSINESS_DIR = ROOT / "business"
REQUIRED_OS = {
    "payroll": "payroll_os.md",
    "sales": "sales_os.md",
    "marketing": "marketing_os.md",
    "bookkeeping": "bookkeeping_os.md",
}


def main() -> None:
    missing = []
    for module, filename in REQUIRED_OS.items():
        path = BUSINESS_DIR / module / filename
        if not path.exists():
            missing.append(str(path))

    if missing:
        raise SystemExit("Missing OS files:\n" + "\n".join(missing))

    print("All module OS files present in neural-core")


if __name__ == "__main__":
    main()
