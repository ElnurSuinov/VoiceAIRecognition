from AIapp.risk.velocity_engine import VelocityEngine
from AIapp.risk.behavior_engine import BehaviorEngine
from AIapp.domain.services.security.device_engine import DeviceEngine
from AIapp.domain.services.security.rule_engine import RuleEngine

class RiskEngine:

    def __init__(self):

        self.velocity = VelocityEngine()
        self.behavior = BehaviorEngine()
        self.device = DeviceEngine()
        self.rules = RuleEngine()

    def evaluate(self, user, amount, request):

        base_risk = self._calculate_amount_risk(amount)

        velocity_risk = self.velocity.evaluate(user)

        behavior_risk = self.behavior.evaluate(user, amount)

        device_risk = self.device.evaluate(user, request)

        rule_risk = self.rules.evaluate(user, amount)

        total_risk = (
            base_risk
            + velocity_risk
            + behavior_risk
            + device_risk
            + rule_risk
        )

        return min(total_risk, 100)

    def _calculate_amount_risk(self, amount):

        amount = float(amount)

        if amount >= 5000:
            return 30

        if amount >= 2000:
            return 15

        return 0