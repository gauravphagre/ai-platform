from app.llm.schemas import ChatMessage
from app.llm.prompts.system import SYSTEM_PROMPT


def build_chat_messages(history):

    messages = [
        ChatMessage(
            role="system",
            content=SYSTEM_PROMPT
        )
    ]

    messages.extend([
        ChatMessage(
            role=msg.role,
            content=msg.content
        )
        for msg in history
    ])

    return messages