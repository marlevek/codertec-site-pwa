document.addEventListener("DOMContentLoaded", () => {

  let context = null;

  // BUTTON
  const btn = document.getElementById("chatbot-btn") || (function () {
    const b = document.createElement("button");
    b.id = "chatbot-btn";
    b.innerHTML = '<img src="/static/images/petshop/petbot.png" alt="PetBot">';
    document.body.appendChild(b);
    return b;
  })();

  // WINDOW
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
        <input id="chatbot-input" type="text" placeholder="Type your message...">
        <button id="chatbot-send">➤</button>
      </div>
    `;
    document.body.appendChild(w);
    return w;
  })();

  const messages = document.getElementById("chatbot-messages");
  const input = document.getElementById("chatbot-input");

  function sendMessage(text, author) {
    const div = document.createElement("div");
    div.className = `msg ${author}`;
    div.innerText = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  sendMessage(
    "Hi! 🐾 I'm Bento 🐶💙\nYour virtual assistant at Pet Love Grooming!\n\nHow can I help you today?\n\nExamples:\n• I want to book\n• Prices\n• Opening hours\n• Address",
    "bot"
  );

  function reply(txt) {
    txt = txt.toLowerCase();

    if (txt.includes("hour") || txt.includes("time") || txt.includes("open")) {
      context = null;
      sendMessage("We’re open from **Monday to Saturday, 9am to 6pm** 🕒", "bot");
      return;
    }

    if (txt.includes("address") || txt.includes("where") || txt.includes("location")) {
      context = null;
      sendMessage("We are at **Rua dos Animais Felizes, 123 — Curitiba** 🐾", "bot");
      return;
    }

    if (txt.includes("bath")) {
      context = "bath";
      sendMessage("Full bath + hydration 🫧🐶\nWhat is your pet’s **name**?", "bot");
      return;
    }

    if (txt.includes("groom") || txt.includes("haircut") || txt.includes("grooming")) {
      context = "grooming";
      sendMessage("We offer puppy cut, hygiene trim and breed-standard grooming ✂️\nWhat is your pet’s **name**?", "bot");
      return;
    }

    if (txt === "yes" || txt.includes("book") || txt.includes("schedule")) {
      context = null;
      sendMessage("Perfect! 😄\nClick here to book via WhatsApp 👉 https://wa.me/5541996131762", "bot");
      return;
    }

    if (context === "bath" || context === "grooming") {
      context = "breed";
      sendMessage("Great! 🐶 What is your pet’s **breed and size**?", "bot");
      return;
    }

    if (context === "breed") {
      context = null;
      sendMessage("Awesome! 💙 I can now estimate the service.\nWould you like to **see available times** now?", "bot");
      return;
    }

    sendMessage(
      "Got it 😊 Tell me, do you need **Bath**, **Grooming**, **Opening hours** or **Address**?",
      "bot"
    );
  }

  btn.onclick = () => box.style.display = "block";
  document.getElementById("close-chat").onclick = () => box.style.display = "none";

  document.getElementById("chatbot-send").onclick = () => {
    const txt = input.value.trim();
    if (!txt) return;
    sendMessage(txt, "user");
    reply(txt);
    input.value = "";
  };

  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      document.getElementById("chatbot-send").click();
    }
  });

});
