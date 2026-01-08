// /static/js/chatbot-loader.js

const pageLang = document.documentElement.lang || "pt";

const CHATBOT_TEXTS = {
  pt: {
    title: "Assistente CoderTec",
    placeholder: "Digite sua mensagem...",
    send: "Enviar"
  },
  en: {
    title: "CoderTec Assistant",
    placeholder: "Type your message...",
    send: "Send"
  },
  es: {
    title: "Asistente CoderTec",
    placeholder: "Escribe tu mensaje...",
    send: "Enviar"
  }
};

const t = CHATBOT_TEXTS[pageLang] || CHATBOT_TEXTS.pt;


(async function loadChatbot() {
  try {
    console.log("💬 [Loader] Iniciando carregamento do chatbot...");

    // -----------------------------------------------------
    // 🔎 Detectar idioma pela URL
    // -----------------------------------------------------
    const path = window.location.pathname.toLowerCase();

    if (path.includes("/en/")) {
      window.CHATBOT_LANG = "en";
    } else if (path.includes("/es/")) {
      window.CHATBOT_LANG = "es";
    } else {
      window.CHATBOT_LANG = "pt";
    }

    console.log("🌎 [Loader] Idioma detectado:", window.CHATBOT_LANG);

    // -----------------------------------------------------
    // 💬 Saudações por idioma
    // -----------------------------------------------------
    const greetings = {
      pt: "Olá! 👋 Sou o assistente virtual da CoderTec. Como posso ajudar?",
      en: "Hello! 👋 I'm the CoderTec virtual assistant. How can I help you today?",
      es: "¡Hola! 👋 Soy el asistente virtual de CoderTec. ¿En qué puedo ayudarte hoy?"
    };

    // -----------------------------------------------------
    // 🌐 Criar (ou reaproveitar) objeto global de contexto
    // -----------------------------------------------------
    if (!window.CHATBOT_CONTEXT || typeof window.CHATBOT_CONTEXT !== "object") {
      window.CHATBOT_CONTEXT = {};
    }

    window.CHATBOT_CONTEXT.language = window.CHATBOT_LANG;
    window.CHATBOT_CONTEXT.greeting = greetings[window.CHATBOT_LANG];

    // -----------------------------------------------------
    // 🧠 Detectar contexto automático por página
    // -----------------------------------------------------
    let detectedContext = "general";

    if (path.includes("automation") || path.includes("automacao") || path.includes("automatizacion")) {
      detectedContext = "automation";
    } else if (path.includes("dash")) {
      detectedContext = "dashboards";
    } else if (path.includes("ai") || path.includes("inteligencia")) {
      detectedContext = "ai";
    } else if (path.includes("web")) {
      detectedContext = "web-development";
    }

    window.CHATBOT_CONTEXT.pageContext = detectedContext;

    console.log("📌 Contexto final:", window.CHATBOT_CONTEXT);

    // -----------------------------------------------------
    // 📥 Carregar HTML do Chatbot
    // -----------------------------------------------------
    const basePath = "/static/components/chatbot.html";
    const res = await fetch(basePath);

    if (!res.ok) throw new Error(`Erro ao carregar chatbot.html (${res.status})`);

    const html = await res.text();
    document.body.insertAdjacentHTML("beforeend", html);
    console.log("✅ [Loader] Chatbot HTML injetado com sucesso.");

    // -----------------------------------------------------
    // ▶️ Aguarda botão aparecer e carrega chatbot.js
    // -----------------------------------------------------
    const waitForButton = setInterval(() => {
      const btn = document.getElementById("chatbot-btn");
      if (!btn) return;

      clearInterval(waitForButton);
      console.log("✅ [Loader] Botão detectado. Carregando chatbot.js...");

      const script = document.createElement("script");
      script.src = "/static/js/chatbot.js?v=3";
      script.defer = true;

      script.onload = () => console.log("🚀 chatbot.js carregado!");
      script.onerror = () => console.error("❌ Erro ao carregar chatbot.js");

      document.body.appendChild(script);
    }, 300);

  } catch (err) {
    console.error("❌ [Loader] Erro ao carregar chatbot:", err);
  }
})();
