import { initModals } from "./modals.js";
import { initMenu } from "./menu.js";
import { initTheme } from "./theme.js";
import { initMatchActions } from "./action.js";
import { initSearchPage } from "./search.js";
import { mountFriendButton } from "./friends.js";
import { initNotificationsPage } from "./notifications.js";
import { initNotifBadge } from "./notif-badge.js"
import { initChatBadge } from "./chat-badge.js";

document.addEventListener("DOMContentLoaded", () => {
  const page = document.body.dataset.page;

  initModals(page);
  initMenu();
  initTheme();
  initMatchActions(page);
  initSearchPage();
  initNotifBadge();
  initChatBadge();

  // Botão de amizade só no perfil
  if (window.profileUserId) {
    mountFriendButton(window.profileUserId);
  }

  // Somente na página de notificações
  if (page === "notifications") {
    initNotificationsPage();
  }
});
