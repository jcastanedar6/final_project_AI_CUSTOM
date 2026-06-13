from backend.cag import apply_context
from backend.knowledge import retrieve_snippets

_CHUNK_MAX_CHARS = 500


def _focused_content(content, max_chars=_CHUNK_MAX_CHARS):
    """Return the first coherent prose block up to max_chars."""
    if len(content) <= max_chars:
        return content
    cutoff = content.rfind(".", 0, max_chars)
    return content[: cutoff + 1] if cutoff > 0 else content[:max_chars]


def answer_question(user_id, question, context_items=None):
    context_items = context_items or []
    snippets = retrieve_snippets(question)

    if not snippets:
        return {
            "user_id": user_id,
            "answer": "No encontre informacion suficiente en la base de conocimiento del curso sobre ese tema.",
            "sources": [],
            "context_used": [],
        }

    parts = []
    for item in snippets:
        focused = _focused_content(item["content"])
        parts.append(f"[{item['title']}]\n{focused}")

    base_answer = "\n\n".join(parts)
    answer = apply_context(user_id, question, base_answer, context_items)

    return {
        "user_id": user_id,
        "answer": answer,
        "sources": [item["id"] for item in snippets],
        "context_used": [item["key"] for item in context_items],
    }
