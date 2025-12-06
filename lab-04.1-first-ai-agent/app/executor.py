from typing import Any, Callable, Dict


class SafeExecutor:
    """
    A very small "tool execution sandbox".

    In production (paid lab), this becomes a proper
    sandbox with permissions, rate limiting, audit logging, etc.
    """

    def run(self, tool_fn: Callable[..., Any], params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = tool_fn(**params)
            return {"ok": True, "result": result}
        except TypeError as e:
            # Parameter mismatch or programming error
            return {"ok": False, "error": f"Parameter error: {e}"}
        except Exception as e:  # pragma: no cover - generic safety net
            return {"ok": False, "error": f"Tool execution failed: {e}"}
