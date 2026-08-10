from typing import List, Dict


class ChatMemory:
    """
    Generic in-memory conversation history manager.

    Keeps recent messages and provides conversation context
    for resolving follow-up questions.
    """

    def __init__(self, max_messages: int = 20):
        self.history: List[Dict[str, str]] = []
        self.max_messages = max_messages

    def add_message(
        self,
        role: str,
        content: str
    ):
        self.history.append(
            {
                "role": role,
                "content": content
            }
        )

        if len(self.history) > self.max_messages:
            self.history = self.history[-self.max_messages:]

    def get_history(self):
        return self.history

    def clear(self):
        self.history.clear()

    def format_history(
        self,
        max_messages: int = 10
    ):
        if not self.history:
            return ""

        recent_history = self.history[-max_messages:]

        history_text = ""

        for message in recent_history:
            history_text += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

        return history_text

    def get_conversation_context(
        self,
        max_messages: int = 6
    ):
        """
        Return the most recent conversation context.

        This is intentionally generic and does not depend on
        any particular resume, project, person, or document.
        """

        if not self.history:
            return ""

        recent_history = self.history[-max_messages:]

        context_lines = []

        for message in recent_history:
            role = message.get("role", "").upper()
            content = message.get("content", "").strip()

            if not content:
                continue

            context_lines.append(
                f"{role}: {content}"
            )

        return "\n".join(context_lines)


memory = ChatMemory()
