"""
Sample alert payloads for quick manual testing or demo.
These are not used directly by the API but helpful for REPL / docs.
"""

HIGH_CPU_ALERT = {
    "type": "high_cpu",
    "service": "payment-api",
}

HIGH_MEMORY_ALERT = {
    "type": "high_memory",
    "service": "web-app",
}

GENERIC_ALERT = {
    "type": "unknown",
    "service": "some-service",
}
