from ai.approvals.approval_engine import ApprovalEngine
from ai.guardrails import Guardrails
from ai.state_machine import StateMachine


class L6Orchestrator:
    def __init__(self, module) -> None:
        self.module = module
        self.state_machine = StateMachine()
        self.guardrails = Guardrails()
        self.approvals = ApprovalEngine()

    def run(self, task: dict) -> None:
        state = "observe"

        while state is not None:
            print(f"STATE: {state}")
            self.guardrails.check(state, task)

            if state == "plan":
                plan = self.module.generate_plan(task)
                self.approvals.request(plan)

            if state == "execute":
                self.module.execute(task)

            if state == "audit":
                self.module.audit(task)
                break

            state = self.state_machine.next(state)
