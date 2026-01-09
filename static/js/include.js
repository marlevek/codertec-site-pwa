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
  // Evita duplicar
  if (document.getElementById("chatbot-loader-script")) return;

  const script = document.createElement("script");
  script.id = "chatbot-loader-script";
  script.src = "/static/js/chatbot-loader.js";
  script.defer = true;
  document.body.appendChild(script);

  script.onload = () =>
    console.log("💬 Chatbot loader carregado e executado com sucesso!");
  script.onerror = () => console.error("❌ Erro ao carregar chatbot-loader.js");

  document.dispatchEvent(new Event("partialsLoaded"));
}


