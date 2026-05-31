def estimate_tokens(text: str) -> int:
    """
    Rough token estimation.
    Later replace with tiktoken or proper tokenizer.
    """

    return int(len(text.split()) * 1.3)


def estimate_message_tokens(messages: list[dict]) -> int:
    total = 0

    for message in messages:
        total += estimate_tokens(message.get("content", ""))

    return total