import pytest

from app.services import chat_service
from app.services.llm_service import LLMUnavailableError


@pytest.fixture()
def replies(monkeypatch):
    """Fake the AI: records the history it receives and answers in order."""
    calls: list[list[dict]] = []
    answers = iter(["Hi Doris, how can I help?", "Here is a plan.", "Third reply."])

    def fake_generate_reply(history):
        calls.append(history)
        return next(answers)

    monkeypatch.setattr(chat_service, "generate_reply", fake_generate_reply)
    return calls


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_serves_the_web_app_from_the_same_server(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>Mira Assistant</title>" in response.text


def test_chat_starts_a_session_and_stores_both_messages(client, replies):
    response = client.post("/api/chat", json={"message": "  Hello Mira  "})

    assert response.status_code == 200
    body = response.json()
    assert body["user_message"] == "Hello Mira"
    assert body["assistant_message"] == "Hi Doris, how can I help?"
    assert replies[0] == [{"role": "user", "content": "Hello Mira"}]

    session = client.get(f"/api/sessions/{body['session_id']}").json()
    assert session["title"] == "Hello Mira"
    assert [(m["role"], m["content"]) for m in session["messages"]] == [
        ("user", "Hello Mira"),
        ("assistant", "Hi Doris, how can I help?"),
    ]


def test_follow_up_sends_the_conversation_history(client, replies):
    first = client.post("/api/chat", json={"message": "Hello Mira"}).json()

    client.post(
        "/api/chat",
        json={"session_id": first["session_id"], "message": "Plan my week"},
    )

    assert replies[1] == [
        {"role": "user", "content": "Hello Mira"},
        {"role": "assistant", "content": "Hi Doris, how can I help?"},
        {"role": "user", "content": "Plan my week"},
    ]


def test_unknown_session_starts_a_new_one(client, replies):
    response = client.post("/api/chat", json={"session_id": 999, "message": "Hi"})

    assert response.status_code == 200
    assert response.json()["session_id"] != 999


def test_failed_ai_reply_returns_a_clear_error_and_saves_nothing(client, monkeypatch):
    def failing_reply(history):
        raise LLMUnavailableError("provider down")

    monkeypatch.setattr(chat_service, "generate_reply", failing_reply)

    response = client.post("/api/chat", json={"message": "Hello"})

    assert response.status_code == 502
    assert "couldn't reach the AI service" in response.json()["detail"]
    assert client.get("/api/sessions").json() == []


def test_without_an_api_key_mira_explains_demo_mode(client):
    response = client.post("/api/chat", json={"message": "Hello"})

    assert response.status_code == 200
    assert "demo mode" in response.json()["assistant_message"]


def test_sessions_list_newest_first_and_missing_session_is_404(client, replies):
    client.post("/api/chat", json={"message": "First chat"})
    client.post("/api/chat", json={"message": "Second chat"})

    titles = [s["title"] for s in client.get("/api/sessions").json()]

    assert titles == ["Second chat", "First chat"]
    assert client.get("/api/sessions/999").status_code == 404


def test_memory_is_saved_and_updated_by_key(client):
    client.post("/api/memory", json={"key": "name", "value": "Doris"})
    client.post("/api/memory", json={"key": "name", "value": "Doris Agusiobo Echianu"})

    assert client.get("/api/memory").json() == [
        {"key": "name", "value": "Doris Agusiobo Echianu"}
    ]


def test_rejects_an_empty_message(client):
    assert client.post("/api/chat", json={"message": ""}).status_code == 422
