export function initModals(page){
  const plusBtn = document.getElementById("action-button");
  const modalCreate = document.getElementById("modal-create-match");
  const modalResult = document.getElementById("modal-update-result");

  const show = modal => modal?.classList.add("visible");
  const hide = modal => modal?.classList.remove("visible");

  const toggle = () => {
    if (page === "match-view") {
      show(modalResult);
    } else {
      show(modalCreate);
    }
    if (plusBtn) {
      plusBtn.classList.remove("animate");
      void plusBtn.offsetWidth;
      plusBtn.classList.add("animate");
    }
  };

  plusBtn?.addEventListener("click", toggle);

  const modals = [modalCreate, modalResult];

  document.querySelectorAll("[data-close]").forEach(btn =>
    btn.addEventListener("click", () => {
      modals.forEach(hide);
    })
  );

  modals.forEach(modal =>
    modal?.addEventListener("click", event => {
      if (event.target === modal) {
        hide(modal);
      }
    })
  );

  document.addEventListener("keydown", event => {
    if (event.key === "Escape") {
      modals.forEach(hide);
    }
  });
}
