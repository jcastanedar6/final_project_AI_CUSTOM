import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from behave import given, then, when


def _url(context, path):
    return f"http://127.0.0.1:{context.port}{path}"


def _get(context, path):
    try:
        with urlopen(_url(context, path), timeout=5) as r:
            return r.status, json.loads(r.read().decode())
    except HTTPError as e:
        body = json.loads(e.read().decode())
        e.close()
        return e.code, body


def _post(context, path, payload):
    req = Request(
        _url(context, path),
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=5) as r:
            return r.status, json.loads(r.read().decode())
    except HTTPError as e:
        body = json.loads(e.read().decode())
        e.close()
        return e.code, body


# ── Given ────────────────────────────────────────────────────────────────────

@given("the server is running")
def step_server_running(context):
    pass  # server lifecycle managed in environment.py


@given('user "{user_id}" has context "{key}" set to "{value}"')
def step_preset_context(context, user_id, key, value):
    status, _ = _post(context, "/api/context", {"user_id": user_id, "key": key, "value": value})
    assert status == 201, f"Pre-condition failed: could not save context (got {status})"


# ── When ─────────────────────────────────────────────────────────────────────

@when('I request GET "{path}"')
def step_get(context, path):
    context.status, context.body = _get(context, path)


@when('I post to "{path}" with body {raw_body}')
def step_post_raw(context, path, raw_body):
    payload = json.loads(raw_body)
    context.status, context.body = _post(context, path, payload)


@when('user "{user_id}" asks "{question}"')
def step_ask(context, user_id, question):
    context.status, context.body = _post(
        context, "/api/ask", {"user_id": user_id, "question": question}
    )


@when('I save context for user "{user_id}" key "{key}" value "{value}"')
def step_save_context(context, user_id, key, value):
    context.status, context.body = _post(
        context, "/api/context", {"user_id": user_id, "key": key, "value": value}
    )


@when('I retrieve context for user "{user_id}"')
def step_get_context(context, user_id):
    context.status, context.body = _get(context, f"/api/context?user_id={user_id}")


# ── Then ─────────────────────────────────────────────────────────────────────

@then("the response status is {code:d}")
def step_status(context, code):
    assert context.status == code, f"Expected {code}, got {context.status}. Body: {context.body}"


@then('the response field "{field}" equals "{value}"')
def step_field_equals_str(context, field, value):
    actual = context.body.get(field)
    assert actual == value, f"Expected body['{field}'] == '{value}', got {actual!r}"


@then('the response field "{field}" equals true')
def step_field_equals_true(context, field):
    actual = context.body.get(field)
    assert actual is True, f"Expected body['{field}'] == True, got {actual!r}"


@then('the answer contains "{fragment}"')
def step_answer_contains(context, fragment):
    answer = context.body.get("answer", "")
    assert fragment.lower() in answer.lower(), f"Expected '{fragment}' in answer, got: {answer!r}"


@then('the sources include "{source_id}"')
def step_sources_include(context, source_id):
    sources = context.body.get("sources", [])
    assert source_id in sources, f"Expected '{source_id}' in sources {sources}"


@then("context_used is empty")
def step_context_used_empty(context):
    ctx = context.body.get("context_used", [])
    assert ctx == [], f"Expected context_used to be empty, got {ctx}"


@then('the context_used includes "{key}"')
def step_context_used_includes(context, key):
    ctx = context.body.get("context_used", [])
    assert key in ctx, f"Expected '{key}' in context_used {ctx}"


@then('the context list contains key "{key}" with value "{value}"')
def step_context_list_contains(context, key, value):
    items = context.body.get("context", [])
    assert {"key": key, "value": value} in items, (
        f"Expected {{key: '{key}', value: '{value}'}} in context {items}"
    )


@then("the context list is empty")
def step_context_list_empty(context):
    items = context.body.get("context", [])
    assert items == [], f"Expected empty context list, got {items}"


@then('the context list has exactly 1 item for key "{key}"')
def step_context_list_one_key(context, key):
    items = context.body.get("context", [])
    matching = [i for i in items if i["key"] == key]
    assert len(matching) == 1, f"Expected 1 item with key '{key}', found {matching}"
