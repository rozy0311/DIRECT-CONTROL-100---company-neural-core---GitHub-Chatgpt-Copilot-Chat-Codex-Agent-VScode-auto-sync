class RiskChecker:
    def check(self, state: str, payload: dict | None) -> None:
        if payload is None:
            return

        risk = payload.get("risk", "low")
        if risk not in {"low", "medium", "high"}:
            raise ValueError(f"Invalid risk level '{risk}' at state {state}")

        if risk == "high":
            raise PermissionError("High risk payload blocked pending manual review")
