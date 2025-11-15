class StateMachine:
    states = [
        "observe",
        "diagnose",
        "plan",
        "approve",
        "execute",
        "audit",
    ]

    transitions = {
        "observe": "diagnose",
        "diagnose": "plan",
        "plan": "approve",
        "approve": "execute",
        "execute": "audit",
        "audit": "observe",
    }

    def next(self, current: str) -> str | None:
        return self.transitions.get(current)
