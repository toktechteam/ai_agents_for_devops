from prometheus_client import Counter, Gauge

agent_requests_total = Counter(
    "agent_requests_total",
    "Total number of requests handled by the agent"
)

agent_tokens_total = Counter(
    "agent_tokens_total",
    "Total number of tokens consumed"
)

agent_average_cost = Gauge(
    "agent_average_cost",
    "Average cost of an investigation (USD)"
)
