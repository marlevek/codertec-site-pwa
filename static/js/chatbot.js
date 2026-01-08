// /static/js/chatbot.js
(function () {
  console.log("🤖 [Chatbot] Script carregado — aguardando HTML...");

  const waitForElements = setInterval(() => {
    if (document.getElementById("chatbot-btn") &&
      document.getElementById("chatbot-window")) {
      clearInterval(waitForElements);
      console.log("✅ [Chatbot] HTML detectado. Iniciando...");
      initChatbot();
    }
  }, 200);

  function initChatbot() {
    const LANG = window.CHATBOT_LANG || "pt";

    // 📌 Novo ➜ agora CHATBOT_CONTEXT é um objeto!
    const CONTEXT = window.CHATBOT_CONTEXT?.pageContext || "general";
    const CUSTOM_GREETING = window.CHATBOT_CONTEXT?.greeting || null;

    console.log("🌎 Idioma:", LANG, "| Contexto:", CONTEXT, "| Custom greeting:", CUSTOM_GREETING);

    // ELEMENTOS
    const chatBtn = document.getElementById("chatbot-btn");
    const chatWindow = document.getElementById("chatbot-window");
    const chatMessages = document.getElementById("chatbot-messages");
    const chatInput = document.getElementById("chatbot-input");
    const chatSend = document.getElementById("chatbot-send");
    const chatClose = document.getElementById("chatbot-close");
    const chatClear = document.getElementById("chatbot-clear");

    // -----------------------------------------------------
    // 🌍 Textos da interface (UI) por idioma
    // -----------------------------------------------------
    const UI_TEXT = {
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

    const ui = UI_TEXT[LANG] || UI_TEXT.pt;

    // Aplica textos na UI
    const chatTitle = document.querySelector(".chatbot-title");
    if (chatTitle) chatTitle.innerText = ui.title;

    if (chatInput) chatInput.placeholder = ui.placeholder;
    if (chatSend) chatSend.innerText = ui.send;


    let greeted = false;
    let userName = "";
    let businessType = "";
    let step = "start";

    const soundSend = new Audio("/static/sounds/send.mp3");
    const soundReceive = new Audio("/static/sounds/receive.mp3");

    // SAUDAÇÕES PT / EN
    const GREET = {
      en: {
        ai: "Hello! 👋 Looking into AI solutions? Want help applying AI to your business?",
        automation: "Hi! 👋 Checking automation? I can help you improve productivity!",
        dashboards: "Hello! 👋 Want to learn how dashboards can help your business?",
        "web-development": "Hi! 👋 I can help you build a modern website or system!",
        general: "Hello! 👋 I'm CoderTec's virtual assistant. How can I help you today?"
      },
      pt: {
        ai: "Olá! 👋 Quer saber como aplicar IA no seu negócio?",
        automacao: "Oi! 👋 Quer automatizar processos e ganhar tempo?",
        dashboards: "Olá! 👋 Quer transformar dados em decisões inteligentes?",
        "web-development": "Oi! 👋 Precisa de um site moderno ou sistema web?",
        general: "Olá! 👋 Sou o assistente da CoderTec. Como posso ajudar hoje?"
      },
      es: {
        ai: "¡Hola! 👋 ¿Quieres saber cómo aplicar IA en tu negocio?",
        automacao: "¡Hola! 👋 ¿Buscas automatizar procesos y ganar tiempo?",
        dashboards: "¡Hola! 👋 ¿Quieres ver cómo los dashboards pueden ayudar a tu empresa?",
        "web-development": "¡Hola! 👋 ¿Necesitas un sitio o sistema web moderno?",
        general: "¡Hola! 👋 Soy el asistente virtual de CoderTec. ¿En qué puedo ayudarte hoy?"
      }
    };

    // FLUXO DE MENSAGENS
    const M = {
      askName:
        LANG === "en"
          ? "Before we start, may I know your name? 😊"
          : LANG === "es"
            ? "Antes de comenzar, ¿puedo saber tu nombre? 😊"
            : "Antes de começarmos, posso saber seu nome? 😊",

      askBusiness: name =>
        LANG === "en"
          ? `Nice to meet you, ${name}! 😄 What type of business do you have?`
          : LANG === "es"
            ? `¡Mucho gusto, ${name}! 😄 ¿En qué área trabajas?`
            : `Prazer, ${name}! 😄 Qual é o seu ramo de atuação?`,

      askService: business =>
        LANG === "en"
          ? `What would you like to build for your ${business}? A website, automation, or an AI solution?`
          : LANG === "es"
            ? `¿Qué te gustaría desarrollar para tu ${business}? ¿Un sitio web, automatización o una solución de IA?`
            : `O que você gostaria de desenvolver para a sua ${business}? Um site, automação ou solução de IA?`,

      askContact: name =>
        LANG === "en"
          ? `All right, ${name}! If you want, I can guide you with more examples.`
          : LANG === "es"
            ? `Perfecto, ${name}! Si quieres, puedo darte más ejemplos o ayudarte con ideas.`
            : `Perfeito, ${name}! Posso te ajudar com mais detalhes ou exemplos, se quiser.`
    };

    //----------------------------------------------------------------
    // ABRIR JANELA
    //----------------------------------------------------------------
    chatBtn.addEventListener("click", () => {
      const visible = chatWindow.style.display === "flex";
      chatWindow.style.display = visible ? "none" : "flex";

      if (!greeted) {
        if (CUSTOM_GREETING) {
          appendMessage(CUSTOM_GREETING, "bot");
        } else {
          const greeting =
            GREET[LANG][CONTEXT] ||
            GREET[LANG].general ||
            "Olá! 👋 Seja bem-vindo!";
          appendMessage(greeting, "bot");
        }
        greeted = true;
      }
    });

    chatClose.addEventListener("click", () => {
      chatWindow.style.display = "none";
    });

    //----------------------------------------------------------------
    // FLUXO PERSONALIZADO
    //----------------------------------------------------------------
    function handleCustomFlow(text) {
      const lower = text.toLowerCase();

      if (step === "start") {
        appendMessage(M.askName, "bot");
        step = "ask_name";
        return true;
      }

      if (step === "ask_name") {
        userName = text.split(" ")[0];
        appendMessage(M.askBusiness(userName), "bot");
        step = "ask_business";
        return true;
      }

      if (step === "ask_business") {
        businessType = text;
        appendMessage(M.askService(businessType), "bot");
        step = "ask_service";
        return true;
      }

      if (step === "ask_service") {
        appendMessage(M.askContact(userName), "bot");
        step = "done";
        return true;
      }

      return false;
    }

    //----------------------------------------------------------------
    // ENVIAR MENSAGEM
    //----------------------------------------------------------------
    chatSend.addEventListener("click", sendMessage);
    chatInput.addEventListener("keypress", e => {
      if (e.key === "Enter") sendMessage();
    });

    async function sendMessage() {
      const text = chatInput.value.trim();
      if (!text) return;

      appendMessage(text, "user");
      chatInput.value = "";

      if (handleCustomFlow(text)) return;

      appendMessage(
        LANG === "en"
          ? "Let me think... 🤖"
          : LANG === "es"
            ? "Déjame pensar... 🤖"
            : "Deixa eu pensar... 🤖",
        "bot"
      );
    }

    //----------------------------------------------------------------
    // EXIBIR MENSAGEM
    //----------------------------------------------------------------
    function appendMessage(text, sender) {
      const wrap = document.createElement("div");
      wrap.classList.add("message-container", sender);

      const avatar = document.createElement("div");
      avatar.classList.add("avatar");
      avatar.innerHTML =
        sender === "user"
          ? '<i class="bi bi-person-circle"></i>'
          : '<i class="bi bi-robot"></i>';

      const msg = document.createElement("div");
      msg.classList.add(
        "message",
        sender === "user" ? "user-message" : "bot-message"
      );
      msg.innerHTML = text;

      wrap.appendChild(avatar);
      wrap.appendChild(msg);
      chatMessages.appendChild(wrap);
      chatMessages.scrollTop = chatMessages.scrollHeight;

      (sender === "user" ? soundSend : soundReceive).play();
    }
  }
})();
