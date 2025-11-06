export function initTheme() {
  const saved = localStorage.getItem("superdegen-theme") || "dark";
  document.documentElement.dataset.theme = saved;

  const toggleTheme = document.getElementById("toggle-theme");
  toggleTheme?.addEventListener("click", () => {
    const isLight = document.documentElement.dataset.theme === "light";
    document.documentElement.dataset.theme = isLight ? "dark" : "light";
    localStorage.setItem("superdegen-theme", document.documentElement.dataset.theme);
  });
}
