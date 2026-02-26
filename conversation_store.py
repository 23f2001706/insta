"""
Simple in-memory conversation store.
For production, replace with Redis or a database.
"""
from collections import defaultdict, deque
from datetime import datetime


class ConversationStore:
    def __init__(self, max_history: int = 20):
        self.max_history = max_history
        self._store: dict[str, deque] = defaultdict(
            lambda: deque(maxlen=max_history)
        )
        self._user_info: dict[str, dict] = {}

    def add_message(self, user_id: str, role: str, content: str):
        """Add a message to conversation history."""
        self._store[user_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def get_history(self, user_id: str) -> list[dict]:
        """Get conversation history for a user."""
        return list(self._store[user_id])

    def clear_history(self, user_id: str):
        """Clear conversation history for a user."""
        self._store[user_id].clear()

    def set_user_info(self, user_id: str, info: dict):
        """Cache user profile info."""
        self._user_info[user_id] = info

    def get_user_info(self, user_id: str) -> dict | None:
        return self._user_info.get(user_id)


# Singleton instance
conversation_store = ConversationStore()