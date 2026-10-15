// The backend serves this page, so API calls go to the same origin.
const API_BASE = "";

const orb = document.getElementById("orb");
const assistantState = document.getElementById("assistantState");
const transcriptBox = document.getElementById("transcript");
const responseBox = document.getElementById("response");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const listenBtn = document.getElementById("listenBtn");
const stopSpeakBtn = document.getElementById("stopSpeakBtn");
const newChatBtn = document.getElementById("newChatBtn");
const sessionList = document.getElementById("sessionList");

let sessionId = null;
let recognition = null;

function setState(state) {
  orb.className = `orb ${state}`;
  assistantState.textContent = state.charAt(0).toUpperCase() + state.slice(1);
}

async function sendMessage(message) {
  if (!message || !message.trim()) return;

  transcriptBox.textContent = message;
  setState("thinking");

  try {
    const response = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message })
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(data.detail || "Something went wrong while contacting the Mira backend.");
    }

    sessionId = data.session_id;
    responseBox.textContent = data.assistant_message;
    await fetchSessions();
    speakText(data.assistant_message);
  } catch (error) {
    console.error(error);
    setState("error");
    responseBox.textContent =
      error instanceof TypeError ? "Mira's server isn't reachable. Is the backend running?" : error.message;
  }
}

function speakText(text) {
  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.onstart = () => setState("speaking");
  utterance.onend = () => setState("idle");
  utterance.onerror = () => setState("error");

  window.speechSynthesis.speak(utterance);
}

function initSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    listenBtn.disabled = true;
    listenBtn.textContent = "Speech Not Supported";
    return;
  }

  recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {
    setState("listening");
    transcriptBox.textContent = "Listening...";
  };

  recognition.onresult = (event) => {
    setState("recognizing");
    const text = event.results[0][0].transcript;
    transcriptBox.textContent = text;
    sendMessage(text);
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    setState("error");
    transcriptBox.textContent = `Speech recognition error: ${event.error}`;
  };

  recognition.onend = () => {
    if (assistantState.textContent === "Listening") {
      setState("idle");
    }
  };
}

async function fetchSessions() {
  try {
    const response = await fetch(`${API_BASE}/api/sessions`);
    if (!response.ok) return;
    const sessions = await response.json();
    renderSessions(sessions);
  } catch (error) {
    console.error("Could not fetch sessions", error);
  }
}

function renderSessions(sessions) {
  sessionList.innerHTML = "";

  if (!sessions.length) {
    sessionList.innerHTML = `<div class="session-item"><div class="session-item-title">No conversations yet</div><div class="session-item-meta">Start your first chat with Mira</div></div>`;
    return;
  }

  sessions.forEach((session) => {
    const item = document.createElement("div");
    item.className = `session-item ${session.id === sessionId ? "active" : ""}`;
    item.innerHTML = `
      <div class="session-item-title">${escapeHtml(session.title || "Untitled")}</div>
      <div class="session-item-meta">${new Date(session.created_at).toLocaleString()}</div>
    `;
    item.addEventListener("click", () => loadSession(session.id));
    sessionList.appendChild(item);
  });
}

async function loadSession(id) {
  try {
    const response = await fetch(`${API_BASE}/api/sessions/${id}`);
    if (!response.ok) throw new Error("Could not load session");

    const session = await response.json();
    sessionId = session.id;

    const lastUser = [...session.messages].reverse().find((msg) => msg.role === "user");
    const lastAssistant = [...session.messages].reverse().find((msg) => msg.role === "assistant");

    transcriptBox.textContent = lastUser ? lastUser.content : "No user message found.";
    responseBox.textContent = lastAssistant ? lastAssistant.content : "No assistant message found.";
    setState("idle");
    fetchSessions();
  } catch (error) {
    console.error(error);
    setState("error");
  }
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

sendBtn.addEventListener("click", () => {
  const message = messageInput.value.trim();
  if (!message) return;
  messageInput.value = "";
  sendMessage(message);
});

messageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    sendBtn.click();
  }
});

listenBtn.addEventListener("click", () => {
  if (recognition) recognition.start();
});

stopSpeakBtn.addEventListener("click", () => {
  window.speechSynthesis.cancel();
  setState("idle");
});

newChatBtn.addEventListener("click", () => {
  sessionId = null;
  transcriptBox.textContent = "Waiting for input...";
  responseBox.textContent = "Hello. I'm Mira. How can I help you today?";
  setState("idle");
  fetchSessions();
});

initSpeechRecognition();
fetchSessions();
