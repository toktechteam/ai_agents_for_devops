class CostTracker:
    TOKEN_COST = 0.000002

    def __init__(self):
        self.tokens = 0

    def add_tokens(self, n):
        self.tokens += n

    def summary(self):
        return {
            "tokens": self.tokens,
            "usd": round(self.tokens * self.TOKEN_COST, 6)
        }
