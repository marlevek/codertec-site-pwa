document.addEventListener("partialsLoaded", () => {
  const btnTopo = document.getElementById("btnVoltarAoTopo");

  if (!btnTopo) {
    console.warn("Botão voltar ao topo não encontrado");
    return;
  }

  window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
      btnTopo.style.display = "block";
    } else {
      btnTopo.style.display = "none";
    }
  });

  btnTopo.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  });
});
