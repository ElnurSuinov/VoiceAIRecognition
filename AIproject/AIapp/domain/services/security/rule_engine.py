from datetime import datetime

from AIapp.models import RiskRule


class RuleEngine:

    def evaluate(self, user, amount):

        risk = 0

        rules = RiskRule.objects.filter(active=True)

        for rule in rules:

            if self._check_rule(rule, user, amount):
                risk += rule.score

        return risk

    def _check_rule(self, rule, user, amount):

        condition = rule.condition

        if condition == "large_amount":
            return amount > 10000

        if condition == "night_transfer":
            return datetime.now().hour >= 23

        return False