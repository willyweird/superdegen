import { api } from "./action.js";


export function initNotificationsPage() {
  // Delegação: evita precisar recarregar listeners quando elementos mudam
  const container = document.querySelector(".notif-list");
  if (!container) return;

  container.addEventListener("click", async (e) => {
    const acceptBtn = e.target.closest(".btn-accept");
    const declineBtn = e.target.closest(".btn-decline");

    // Aceitar
    if (acceptBtn) {
      const userId = acceptBtn.dataset.id;
      await api(`/social/friendship/accept/${userId}`, { method: "POST" });
      removeItem(acceptBtn);
    }

    // Recusar
    if (declineBtn) {
      const userId = declineBtn.dataset.id;
      await api(`/social/friendship/decline/${userId}`, { method: "POST" });
      removeItem(declineBtn);
    }
  });
}

function removeItem(btn) {
  const item = btn.closest(".notif-item");
  if (!item) return;
  item.classList.add("removing");
  setTimeout(() => item.remove(), 250);
}
