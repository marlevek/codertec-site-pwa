const chatBtn = document.getElementById("chatbot-btn");
const chatWindow = document.getElementById("chatbot-window");
const messages = document.getElementById("chatbot-messages");
const chatInput = document.getElementById("chatbot-input");
const chatSend = document.getElementById("chatbot-send");

function addMessage(text, sender="bot") {
    const msg = document.createElement("div");
    msg.className = "message " + sender;
    msg.innerHTML = text;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
}

const firstMessage = `
Hello! I'm <strong>Sophie</strong>, your virtual assistant 💙<br><br>
How can I help you today?<br><br>
• Skin care treatments<br>
• Aesthetic procedures<br>
• Consultations<br>
• Talk to a specialist
`;

chatBtn.onclick = () => {
    chatWindow.style.display = 
        chatWindow.style.display === "block" ? "none" : "block";

    if (messages.innerHTML.trim() === "")
        addMessage(firstMessage);
};

chatSend.onclick = () => {
    const text = chatInput.value.trim();
    if (!text) return;

    addMessage(text, "user");
    chatInput.value = "";

    setTimeout(() => {
        addMessage("Thank you! I’ll connect you to our specialist shortly.");
    }, 600);
};

document.addEventListener("click", (e) => {
    if (!chatWindow.contains(e.target) &&
        !chatBtn.contains(e.target)) {
        chatWindow.style.display = "none";
    }
});

chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") chatSend.click();
});
