export async function api(path, opts = {}) {
  let body = null;
  let headers = opts.headers || {};

  if (opts.body instanceof FormData) {
    body = opts.body;
  } else if (opts.body && typeof opts.body === "object") {
    body = new FormData();
    for (const key in opts.body) {
      body.append(key, opts.body[key]);
    }
  }

  const response = await fetch(path, {
    method: opts.method || "GET",
    headers,
    body,
  });

  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return response.json();
  }
  return response.text();
}

/* ==============================
   AÇÕES DE MATCHES
================================ */
export function initMatchActions(page) {
  const createBtn = document.getElementById("confirm-create-match");
  createBtn?.addEventListener("click", async () => {
    const titleInput = document.getElementById("match-title-input");
    const opponentsInput = document.getElementById("match-opponents-input");
    const gameInput = document.getElementById("match-game-input");
    const leagueInput = document.getElementById("match-league-input");
    const stageInput = document.getElementById("match-stage-input");
    const statusSelect = document.getElementById("match-status-select");
    const dateInput = document.getElementById("match-date-input");

    titleInput.style.borderColor = "";
    opponentsInput.style.borderColor = "";

    const title = titleInput.value.trim();
    const opponents = opponentsInput.value.trim();

    if (!title) {
      titleInput.focus();
      titleInput.style.borderColor = "var(--accent)";
      return;
    }

    if (!opponents) {
      opponentsInput.focus();
      opponentsInput.style.borderColor = "var(--accent)";
      return;
    }

    const formData = new FormData();
    formData.append("title", title);
    formData.append("opponents", opponents);
    formData.append("game", gameInput.value.trim());
    formData.append("league", leagueInput.value.trim());
    formData.append("stage", stageInput.value.trim());
    formData.append("status", statusSelect.value);
    formData.append("scheduled_for", dateInput.value);

    const result = await api("/matches/create", {
      method: "POST",
      body: formData,
    });

    if (result?.error) {
      alert(result.error);
      return;
    }

    if (result?.success) {
      window.location.href = `/matches/${result.match_id}`;
    }
  });

  const updateBtn = document.getElementById("confirm-update-result");
  if (page === "match-view") {
    const statusSelect = document.getElementById("result-status-select");
    const scoreInput = document.getElementById("result-score-input");
    const summaryInput = document.getElementById("result-summary-input");

    if (statusSelect && window.currentMatchStatus) {
      statusSelect.value = window.currentMatchStatus;
    }
    if (scoreInput) {
      scoreInput.value = window.currentMatchResult || "";
    }
    if (summaryInput) {
      summaryInput.value = window.currentMatchSummary || "";
    }
  }

  updateBtn?.addEventListener("click", async () => {
    const matchId = window.currentMatchId;
    if (!matchId) {
      return;
    }

    const statusSelect = document.getElementById("result-status-select");
    const scoreInput = document.getElementById("result-score-input");
    const summaryInput = document.getElementById("result-summary-input");

    const formData = new FormData();
    formData.append("status", statusSelect.value);
    formData.append("result", scoreInput.value.trim());
    formData.append("summary", summaryInput.value.trim());

    const result = await api(`/matches/${matchId}/result`, {
      method: "POST",
      body: formData,
    });

    if (result?.error) {
      alert(result.error);
      return;
    }

    if (result?.success) {
      window.location.reload();
    }
  });
}
