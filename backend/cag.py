def apply_context(user_id, question, base_answer, context_items):
    if not context_items:
        return base_answer
    context_text = " ".join(item["value"] for item in context_items)
    return f"{base_answer} {context_text}"
