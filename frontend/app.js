const askForm = document.querySelector("#ask-form");
const answerOutput = document.querySelector("#answer-output");
const contextOutput = document.querySelector("#context-output");

const API_BASE_URL = "http://127.0.0.1:8030";

askForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(askForm);
  const payload = {
    user_id: formData.get("user_id"),
    question: formData.get("question"),
  };

  answerOutput.textContent = "Consultando...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    answerOutput.textContent = JSON.stringify(result, null, 2);
    await loadContext(payload.user_id);
  } catch (error) {
    answerOutput.textContent = `No se pudo conectar con el backend: ${error.message}`;
  }
});

async function loadContext(userId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/context?user_id=${encodeURIComponent(userId)}`);
    const result = await response.json();
    contextOutput.textContent = JSON.stringify(result, null, 2);
  } catch (error) {
    contextOutput.textContent = "El modulo CAG aun no esta disponible.";
  }
}
