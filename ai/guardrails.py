from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ai.validators.risk_checker import RiskChecker
from ai.validators.schema_validator import SchemaValidator


@dataclass
class Guardrails:
    schema: SchemaValidator = SchemaValidator()
    risk: RiskChecker = RiskChecker()

    def check(self, state: str, payload: Any) -> None:
        self.schema.validate(state, payload)
        self.risk.check(state, payload)
