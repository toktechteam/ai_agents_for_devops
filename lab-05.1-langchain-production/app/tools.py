class Tools:
    def get_pods(self, service: str) -> str:
        return f"[FAKE] pods for {service}: {service}-123 {service}-456"

    def get_logs(self, service: str) -> str:
        return f"[FAKE] logs for {service}: INFO stable system"

    def get_metrics(self, service: str) -> str:
        return f"[FAKE] metrics: latency_p95=430ms cpu=87%"
