import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
STATE_GRAPH = ROOT / "ai" / "ai_state_graph.json"


def main() -> None:
    if not STATE_GRAPH.exists():
        print("No ai_state_graph.json found; skipping validation")
        return

    with STATE_GRAPH.open("r", encoding="utf-8") as handle:
        graph = json.load(handle)

    states = graph.get("states", [])
    transitions = graph.get("transitions", {})

    if not states or not isinstance(states, list):
        raise SystemExit("State graph must declare a 'states' array")

    for source, target in transitions.items():
        if source not in states or target not in states:
            raise SystemExit(f"Invalid transition {source} -> {target}")

    print(f"Validated state graph with {len(states)} states")


if __name__ == "__main__":
    main()
