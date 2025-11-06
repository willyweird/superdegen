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
   AÇÕES DE ÁLBUNS
================================ */
export function initAlbumActions() {

  /* ========== Criar Álbum ========== */
  const confirmCreateAlbum = document.getElementById("confirm-create-album");
  confirmCreateAlbum?.addEventListener("click", async () => {
    const input = document.getElementById("album-name-input");
    const name = input.value.trim();
    if (!name){
      input.focus();
      input.style.borderColor = "var(--accent)";
      return;
    }

    const formData = new FormData();
    formData.append("name", name);

    const data = await api("/albums/create", {
      method: "POST",
      body: formData
    });

    if (data.success) {
      window.location.href = `/albums/${data.album_id}`;
    }
  });


  /* ========== Upload de Foto ========== */
  const confirmUploadPhoto = document.getElementById("confirm-upload-photo");
  confirmUploadPhoto?.addEventListener("click", async () => {

    const file = document.getElementById("photo-file-input").files[0];
    if (!file) return alert("Selecione uma foto.");

    const albumId = window.location.pathname.split("/").pop();
    const formData = new FormData();
    formData.append("file", file);

    const data = await api(`/albums/upload/${albumId}`, {
      method: "POST",
      body: formData
    });

    if (data.success) {
      window.location.reload();
    }
  });

}
