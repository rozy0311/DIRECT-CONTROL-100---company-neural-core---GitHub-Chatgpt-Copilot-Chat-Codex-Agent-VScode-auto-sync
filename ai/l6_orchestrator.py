import yaml, json, sys
from ai.audit_engine import write_audit
class L6Orchestrator:
    def __init__(self):
        self.rules = yaml.safe_load(open("ai/ai_ruleset.yaml"))
        self.registry = yaml.safe_load(open("ai/module_registry.yaml"))
        self.state_graph = json.load(open("ai/ai_state_graph.json"))
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
    def handle_observe(self, module_id): return "observed"
    def handle_diagnose(self, module_id): return "diagnosed"
    def handle_plan(self, module_id): return "planned"
    def handle_approve(self, module_id): return "approval required"
    def handle_execute(self, module_id): return "executed"
    def handle_audit(self, module_id):
        write_audit(module_id, "changes", "plan", "none"); return "audited"
if __name__ == "__main__":
    module = sys.argv[1] if len(sys.argv)>1 else "bookkeeping"
    L6Orchestrator().run(module)
