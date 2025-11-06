export function initChatBadge(){
  const badge = document.getElementById("chat-badge");
  if (!badge) return;

  async function update(){
    const res = await fetch("/chat/unread_count");
    const count = await res.json();

    if (count > 0){
      badge.style.display = "flex";
      badge.textContent = count;
    } else {
      badge.style.display = "none";
    }
  }

  update();
  setInterval(update, 6000); // atualiza a cada 6s
}
