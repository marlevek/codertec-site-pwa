// /static/js/include.js
async function loadComponent(id, file) {
  try {
    // 🔹 Garante que sempre busca da raiz
    const base = window.location.origin;
    const response = await fetch(`${base}/partials/${file}`);
    if (!response.ok) throw new Error(`Erro ao carregar ${file}`);
    const content = await response.text();
    document.getElementById(id).innerHTML = content;

    // 💬 Se for o footer, carrega o chatbot automaticamente
    if (file === "footer.html") {
      console.log("✅ Footer carregado, iniciando chatbot...");
      injectChatbotLoader();
    }
  } catch (error) {
    console.error("❌ Erro ao carregar componente:", error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadComponent("header", "header.html");
  loadComponent("footer", "footer.html");

  // Hero só se existir
  if (document.getElementById("hero")) {
    loadComponent("hero", "hero.html");
  }
});


function injectChatbotLoader() {
  // Widget AtendeSite — substitui o chatbot antigo da CoderTec.
  // Injetado via createElement para o <script> de fato executar
  // (script colocado por innerHTML no footer NÃO executa).
  if (document.getElementById("atendesite-widget")) return;

  const script = document.createElement("script");
  script.id = "atendesite-widget";
  script.src = "https://api.atendesite.com.br/widget.js";
  script.setAttribute("data-tenant", "codertec");
  script.setAttribute("data-bottom", "170"); // acima do botão de WhatsApp do site
  script.defer = true;
  document.body.appendChild(script);

  document.dispatchEvent(new Event("partialsLoaded"));
}


