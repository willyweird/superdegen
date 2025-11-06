export function initModals(page){

  const plusBtn = document.getElementById("action-button");
  const modalCreate = document.getElementById("modal-create-album");
  const modalUpload = document.getElementById("modal-upload-photo");

  const show = m => m?.classList.add("visible");
  const hide = m => m?.classList.remove("visible");

  plusBtn?.addEventListener("click", () => {
    page === "album-view" ? show(modalUpload) : show(modalCreate);
    plusBtn.classList.remove("animate");
    void plusBtn.offsetWidth;
    plusBtn.classList.add("animate");
  });

  document.querySelectorAll("[data-close]").forEach(btn =>
    btn.addEventListener("click", () => {
      hide(modalCreate);
      hide(modalUpload);
    })
  );

  [modalCreate, modalUpload].forEach(modal =>
    modal?.addEventListener("click", e => {
      if (e.target === modal) hide(modal);
    })
  );

  document.addEventListener("keydown", e => {
    if (e.key === "Escape") {
      hide(modalCreate);
      hide(modalUpload);
    }
  });
}
