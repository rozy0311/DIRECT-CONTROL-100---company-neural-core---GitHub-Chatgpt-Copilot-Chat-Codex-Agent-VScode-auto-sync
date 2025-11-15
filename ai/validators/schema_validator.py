class SchemaValidator:
    def validate(self, state: str, payload: dict | None) -> None:
        if payload is None:
            return

        required = payload.get("required_fields", [])
        data = payload.get("data", {})

        missing = [field for field in required if field not in data]
        if missing:
            raise ValueError(f"Missing required fields at state {state}: {missing}")
