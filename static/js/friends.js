import { api } from "./action.js";

export async function mountFriendButton(userId) {
  const wrap = document.getElementById(`friend-btn-wrap-${userId}`) || document.getElementById("friend-btn-wrap");
  if (!wrap) return;

  const res = await api(`/social/friendship/status/${userId}`);

  const status = res.status;
  const requester = Number(res.requester);
  const current = Number(window.currentUserId);

  let html = "";

  if (status === "none") {
    html = `<button class="friend-btn" data-action="add">Adicionar Amigo</button>`;
  } 
  else if (status === "pending" && requester === current) {
    html = `<button class="friend-btn disabled">Solicitação enviada</button>`;
  } 
  else if (status === "pending" && requester !== current) {
    html = `
      <button class="friend-btn" data-action="accept">Aceitar</button>
      <button class="friend-btn" data-action="decline">Recusar</button>
    `;
  } 
  else if (status === "accepted") {
    html = `<button class="friend-btn" data-action="remove">Amigos ✓</button>`;
  }

  wrap.innerHTML = html;

  wrap.onclick = async (e) => {
    const action = e.target.dataset.action;
    if (!action) return;

    if (action === "add") await api(`/social/friendship/send/${userId}`, { method: "POST" });
    if (action === "accept") await api(`/social/friendship/accept/${userId}`, { method: "POST" });
    if (action === "decline") await api(`/social/friendship/decline/${userId}`, { method: "POST" });
    if (action === "remove") await api(`/social/friendship/remove/${userId}`, { method: "POST" });

    mountFriendButton(userId);
  };
}
