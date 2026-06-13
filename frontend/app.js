const askForm = document.querySelector("#ask-form");
const answerOutput = document.querySelector("#answer-output");
const contextOutput = document.querySelector("#context-output");
const contextForm = document.querySelector("#context-form");
const contextTitle = document.querySelector("#context-title");

const API_BASE_URL = "http://127.0.0.1:8030";

function currentUserId() {
  return document.querySelector("#user-id").value.trim() || "student-01";
}

// ── Ask ──────────────────────────────────────────────────────────────────────

askForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const userId = currentUserId();
  const question = document.querySelector("#question").value.trim();

  setAnswerLoading();

  try {
    const response = await fetch(`${API_BASE_URL}/api/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, question }),
    });
    const result = await response.json();
    renderAnswer(result);
    await loadContext(userId);
  } catch (error) {
    answerOutput.innerHTML = `<p class="answer-error">No se pudo conectar con el backend: ${error.message}</p>`;
  }
});

function setAnswerLoading() {
  answerOutput.innerHTML = `<p class="answer-loading">Consultando...</p>`;
}

function renderAnswer(result) {
  const sourcesHtml = (result.sources || [])
    .map((s) => `<span class="tag">${s}</span>`)
    .join(" ");

  const contextUsedHtml =
    result.context_used && result.context_used.length > 0
      ? `<div class="answer-meta">
           <span class="meta-label">Contexto aplicado:</span>
           ${result.context_used.map((k) => `<span class="tag tag-cag">${k}</span>`).join(" ")}
         </div>`
      : "";

  answerOutput.innerHTML = `
    <p class="answer-text">${result.answer}</p>
    ${sourcesHtml ? `<div class="answer-meta"><span class="meta-label">Fuentes:</span> ${sourcesHtml}</div>` : ""}
    ${contextUsedHtml}
  `;
}

// ── Context panel ─────────────────────────────────────────────────────────────

async function loadContext(userId) {
  contextTitle.textContent = `Contexto — ${userId}`;
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/context?user_id=${encodeURIComponent(userId)}`
    );
    const result = await response.json();
    renderContext(result.context || []);
  } catch {
    contextOutput.innerHTML = `<p class="context-empty">El modulo CAG aun no esta disponible.</p>`;
  }
}

function renderContext(items) {
  if (items.length === 0) {
    contextOutput.innerHTML = `<p class="context-empty">Sin contexto guardado.</p>`;
    return;
  }
  contextOutput.innerHTML = items
    .map(
      (item) => `
      <div class="context-item">
        <span class="ctx-key">${item.key}</span>
        <span class="ctx-value">${item.value}</span>
      </div>`
    )
    .join("");
}

// ── Save context ──────────────────────────────────────────────────────────────

contextForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const userId = currentUserId();
  const key = document.querySelector("#ctx-key").value.trim();
  const value = document.querySelector("#ctx-value").value.trim();

  if (!key || !value) return;

  try {
    await fetch(`${API_BASE_URL}/api/context`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, key, value }),
    });
    document.querySelector("#ctx-key").value = "";
    document.querySelector("#ctx-value").value = "";
    await loadContext(userId);
  } catch (error) {
    console.error("Error guardando contexto:", error);
  }
});

// ── Init: load context for default user ──────────────────────────────────────

document.querySelector("#user-id").addEventListener("change", (e) => {
  loadContext(e.target.value.trim());
});

loadContext(currentUserId());
