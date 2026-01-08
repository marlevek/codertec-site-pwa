document.addEventListener("partialsLoaded", () => {

  const navbarCollapseEl = document.querySelector(".navbar-collapse");
  const navbarToggler = document.querySelector(".navbar-toggler");

  if (!navbarCollapseEl || !navbarToggler || !window.bootstrap) {
    console.warn("Navbar ou Bootstrap não encontrados");
    return;
  }

  // Cria instância oficial do Bootstrap Collapse
  const bsCollapse = new bootstrap.Collapse(navbarCollapseEl, {
    toggle: false
  });

  // Fecha ao clicar em qualquer link do menu
  navbarCollapseEl.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", () => {
      bsCollapse.hide();
    });
  });

  // Fecha ao clicar fora
  document.addEventListener("click", (event) => {
    const isClickInside =
      navbarCollapseEl.contains(event.target) ||
      navbarToggler.contains(event.target);

    if (!isClickInside && navbarCollapseEl.classList.contains("show")) {
      bsCollapse.hide();
    }
  });
});
