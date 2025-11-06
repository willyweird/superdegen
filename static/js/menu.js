export function initMenu() {
  const menuBtn = document.getElementById("menu-button");
  const menu = document.getElementById("side-menu");
  const submenu = document.getElementById("side-submenu");
  const backdrop = document.getElementById("side-menu-backdrop");
  const openPreferences = document.getElementById("open-preferences");
  const closePreferences = document.getElementById("close-submenu");

  menuBtn?.addEventListener("click", () => {
    menu.classList.add("visible");
    backdrop.classList.add("visible");
  });

  backdrop?.addEventListener("click", () => {
    menu.classList.remove("visible");
    submenu.classList.remove("visible");
    backdrop.classList.remove("visible");
  });

  openPreferences?.addEventListener("click", () => {
    menu.classList.remove("visible");
    submenu.classList.add("visible");
  });

  closePreferences?.addEventListener("click", () => {
    submenu.classList.remove("visible");
    menu.classList.add("visible");
  });
}
