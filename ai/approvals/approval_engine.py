class ApprovalEngine:
    def request(self, plan: dict | None) -> None:
        if not plan:
            print("ApprovalEngine: No plan to approve")
            return

        approver = plan.get("approver", "controller")
        print(f"Routing plan to {approver} for approval")
