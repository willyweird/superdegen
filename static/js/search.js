import { api } from "./action.js";
import { mountFriendButton } from "./friends.js";

export function initSearchPage() {
  const input = document.querySelector(".search-input");
  const results = document.getElementById("search-results");
  if (!input || !results) return;

  let timeout;

  input.addEventListener("input", () => {
    clearTimeout(timeout);

    timeout = setTimeout(async () => {
      const q = input.value.trim();
      if (!q) {
        results.innerHTML = "";
        return;
      }

      const users = await api(`/search/users?q=${encodeURIComponent(q)}`);

      results.innerHTML = users.map(u => `
        <div class="search-user-item" data-id="${u.id}">
          <div class="search-user-left">
            <div class="search-user-avatar"
              style="background-image:url('/static/assets/placeholder/placeholder.svg')"></div>
            <div class="search-user-name">@${u.username}</div>
          </div>

          <!-- ✅ Aqui é onde o botão será montado -->
          <div id="friend-btn-wrap-${u.id}" class="friend-btn-wrap"></div>
        </div>
      `).join("");

      // Clique para abrir o perfil
      results.querySelectorAll(".search-user-left").forEach(el => {
        el.addEventListener("click", () => {
          const id = el.closest(".search-user-item").dataset.id;
          window.location.href = `/users/${id}`;
        });
      });

      // ✅ Agora montamos os botões corretos
      users.forEach(u => {
        mountFriendButton(u.id);
      });

    }, 200);
  });
}
