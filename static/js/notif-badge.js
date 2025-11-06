import { api } from "./action.js";

export async function initNotifBadge() {
  const badge = document.getElementById("notif-badge");
  if (!badge) return;

  async function refresh() {
    const count = await api("/notifications/count");
    if (count > 0) {
      badge.textContent = count;
      badge.style.display = "block";
    } else {
      badge.style.display = "none";
    }
  }

  refresh();
  setInterval(refresh, 8000); // atualiza a cada 8s
}
