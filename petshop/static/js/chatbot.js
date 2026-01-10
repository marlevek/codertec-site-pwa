document.addEventListener("DOMContentLoaded", () => {

  let contexto = null; // ← salva o assunto atual da conversa

  const btn = document.getElementById("chatbot-btn") || (function () {
    const b = document.createElement("button");
    b.id = "chatbot-btn";
    b.innerHTML = '<img src="static/images/petbot.png" alt="PetBot">';
    document.body.appendChild(b);
    return b;
  })();

  const box = document.getElementById("chatbot-window") || (function () {
    const w = document.createElement("div");
    w.id = "chatbot-window";
    w.innerHTML = `
      <div id="chatbot-header">
        Bento 🐶 <span>• Online</span>
        <button id="close-chat">×</button>
      </div>
      <div id="chatbot-messages"></div>
      <div id="chatbot-input-area">
        <input id="chatbot-input" type="text" placeholder="Digite...">
        <button id="chatbot-send">➤</button>
      </div>
    `;
    document.body.appendChild(w);
    return w;
  })();

  const messages = document.getElementById("chatbot-messages");
  const input = document.getElementById("chatbot-input");

  function enviar(texto, autor) {
    const div = document.createElement("div");
    div.className = `msg ${autor}`;
    div.innerText = texto;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  // Mensagem inicial
  enviar("Olá! 🐾 Eu sou o Bento 🐶💙\nO assistente virtual do Pet Love Grooming!\n\nComo posso ajudar hoje?\n\nExemplos:\n• Quero agendar\n• Preços\n• Horários\n• Endereço", "bot");

  function responder(txt) {
    txt = txt.toLowerCase();

    // Horários
    if (txt.includes("hor")) {
      contexto = null;
      enviar("Atendemos de **Seg a Sáb**, das **9h às 18h** 🕒", "bot");
      return;
    }

    // Endereço
    if (txt.includes("end")) {
      contexto = null;
      enviar("Estamos na **Rua dos Animais Felizes, 123 — Curitiba** 🐾", "bot");
      return;
    }

    // Solicitação de banho/tosa
    if (txt.includes("banho")) {
      contexto = "banho";
      enviar("Banho completo + hidratação 🫧🐶\nQual o **nome do pet**?", "bot");
      return;
    }

    if (txt.includes("tosa")) {
      contexto = "tosa";
      enviar("Temos tosa bebê, higiênica e padrão da raça ✂️\nQual o **nome do pet**?", "bot");
      return;
    }

    // Depois de dizer "sim" → ir para agendamento se houver contexto
    if (txt === "sim" || txt.includes("agendar")) {
      contexto = null;
      enviar("Perfeito! 😄\nClique aqui para agendar pelo WhatsApp 👉 https://wa.me/5541996131762", "bot");
      return;
    }

    // Se o contexto é banho ou tosa e usuário digitou qualquer coisa → pedir raça
    if (contexto === "banho" || contexto === "tosa") {
      contexto = "raça";
      enviar("Que legal! 🐶 Qual a **raça e tamanho** do seu pet?", "bot");
      return;
    }

    if (contexto === "raça") {
      contexto = null;
      enviar("Show! 💙 Já posso calcular certinho.\nQuer **ver horários disponíveis** agora?", "bot");
      return;
    }

    // Resposta padrão (quando não entendeu)
    enviar("Certo 😊 Me diga, você deseja **Banho**, **Tosa**, **Horários**, ou **Endereço**?", "bot");
  }

  // Botão abre/fecha
  btn.onclick = () => box.style.display = "block";
  document.getElementById("close-chat").onclick = () => box.style.display = "none";

  // Enviar mensagem ao clicar
  document.getElementById("chatbot-send").onclick = () => {
    const txt = input.value.trim();
    if (!txt) return;
    enviar(txt, "user");
    responder(txt);
    input.value = "";
  };

  // ✅ Enviar ao pressionar ENTER
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      document.getElementById("chatbot-send").click();
    }
  });

});
