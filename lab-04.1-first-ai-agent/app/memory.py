from typing import Any, Dict


class Memory:
    """
    Very simple in-process memory to illustrate
    working memory / episodic idea from Chapter 4.

    In paid labs, this evolves into Redis + Postgres + Vector DB.
    """

    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}

    def remember(self, key: str, value: Any) -> None:
        self._store[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)

    def dump(self) -> Dict[str, Any]:
        # For debugging / returning as snapshot
        return dict(self._store)
