import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "data" / "knowledge_base.json"

_STOPWORDS = {
    "que","es","en","el","la","los","las","un","una","de","del","al","se","su","sus",
    "y","o","a","con","por","para","como","pero","si","no","mas","ya","cuando","donde",
    "este","esta","estos","estas","ese","esa","esos","esas","lo","le","les","nos","me",
    "te","mi","tu","hay","son","ser","fue","era","han","has","he","muy","bien","todo",
    "todos","toda","todas","otro","otra","otros","entre","sobre","hasta","desde","antes",
    "cada","sin","solo","tanto","tambien","puede","debe","tiene","hacer","sido","cual",
    "cuales","hacia","durante","segun","vez","veces","tres","dos","uno","quiero","saber",
    "decir","dime","explicame","explica","cuales","podrias","puedes","favor",
}


def load_knowledge_base(path=KNOWLEDGE_BASE_PATH):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


_CODE_RE = re.compile(
    r'(def |class |import |from |>>>|```|\{\"id\"|\[\{)',
    re.IGNORECASE,
)


def _tokenize(text):
    tokens = re.findall(r"[a-záéíóúüñ]{3,}", text.lower())
    return {t for t in tokens if t not in _STOPWORDS}


def _semantic_content(item):
    """Return only the prose portion of a chunk — stops before code blocks."""
    text = f"{item['title']} {item['content']}"
    match = _CODE_RE.search(text)
    return text[: match.start()] if match else text


def retrieve_snippets(question, knowledge_base=None, limit=4):
    knowledge_base = knowledge_base or load_knowledge_base()
    query_terms = _tokenize(question)

    if not query_terms:
        return []

    scored = []
    for item in knowledge_base:
        haystack_terms = _tokenize(_semantic_content(item))
        matches = query_terms & haystack_terms
        if matches:
            # weight: matched terms / total query terms (recall-like score)
            score = len(matches) / len(query_terms)
            scored.append((score, item))

    scored.sort(key=lambda pair: pair[0], reverse=True)

    # Deduplicate: skip chunks whose parent doc is already well-represented
    seen_docs = {}
    result = []
    for score, item in scored:
        doc = item.get("doc", item["id"])
        count = seen_docs.get(doc, 0)
        if count < 2:          # max 2 chunks per source document
            result.append(item)
            seen_docs[doc] = count + 1
        if len(result) >= limit:
            break

    return result
