const chatbotBtn = document.getElementById("chatbot-btn");
const chatbotWindow = document.getElementById("chatbot-window");
const chatbotMessages = document.getElementById("chatbot-messages");
const chatbotInput = document.getElementById("chatbot-input");
const chatbotSend = document.getElementById("chatbot-send");

function addMessage(text, sender = "bot") {
  const msg = document.createElement("div");
  msg.className = "message " + sender;
  msg.innerHTML = text;
  chatbotMessages.appendChild(msg);
  chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

const firstMessage = `
Hello! I'm <strong>Emma</strong>, your virtual assistant 😊<br><br>
How can I help you today?<br><br>
• Dental treatments<br>
• Appointment information<br>
• Talk to a specialist
`;

chatbotBtn.onclick = () => {
  const isOpen = chatbotWindow.style.display === "flex";
  chatbotWindow.style.display = isOpen ? "none" : "flex";   // ✅ flex, não block

  if (!isOpen && chatbotMessages.innerHTML.trim() === "") {
    addMessage(firstMessage);
  }
};

chatbotSend.onclick = () => {
  const text = chatbotInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  chatbotInput.value = "";

  setTimeout(() => {
    addMessage("Thank you! I will connect you to our specialist shortly.");
  }, 600);
};

document.addEventListener("click", (e) => {
  if (!chatbotWindow.contains(e.target) && !chatbotBtn.contains(e.target)) {
    chatbotWindow.style.display = "none";
  }
});

chatbotInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") chatbotSend.click();
});
