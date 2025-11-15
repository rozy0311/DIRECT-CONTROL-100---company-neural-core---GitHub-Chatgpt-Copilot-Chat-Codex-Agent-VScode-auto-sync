import json, pathlib, sys

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import yaml
from ai.audit_engine import write_audit
class L6Orchestrator:
    def __init__(self):
        rules_path = PROJECT_ROOT / "ai" / "ai_ruleset.yaml"
        registry_path = PROJECT_ROOT / "ai" / "module_registry.yaml"
        state_graph_path = PROJECT_ROOT / "ai" / "ai_state_graph.json"

        self.rules = yaml.safe_load(rules_path.read_text(encoding="utf-8"))
        self.registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        self.state_graph = json.loads(state_graph_path.read_text(encoding="utf-8"))
    def run(self, module_id):
        logs = []
        for state in self.state_graph["states"]:
            fn = f"handle_{state}"
            if hasattr(self, fn):
                result = getattr(self, fn)(module_id)
                logs.append([state, result])
                if state == "approve" and self.rules["governance"]["require_approval"]:
                    print(">>> Awaiting approval (yes/no)")
                    return "awaiting_approval"
            else:
                logs.append([state, "no handler"])
        return logs
    def handle_observe(self, module_id): return f"{module_id}:observed"
    def handle_diagnose(self, module_id): return f"{module_id}:diagnosed"
    def handle_plan(self, module_id): return f"{module_id}:planned"
    def handle_approve(self, module_id): return f"{module_id}:approval required"
    def handle_execute(self, module_id): return f"{module_id}:executed"
    def handle_audit(self, module_id):
        write_audit(module_id, "changes", "plan", "none"); return "audited"
if __name__ == "__main__":
    module = sys.argv[1] if len(sys.argv)>1 else "bookkeeping"
    L6Orchestrator().run(module)
