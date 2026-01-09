// /static/js/include_en.js

console.log("🔵 include_en.js carregado!");

async function loadPartial(targetId, fileName) {
    try {
        const url = `/en/partials/${fileName}`;
        console.log(`🔹 Tentando carregar: ${url}`);

        const response = await fetch(url);
        console.log("📡 Status:", response.status);

        if (!response.ok) throw new Error(`Falha ao carregar ${url}`);

        const html = await response.text();
        document.getElementById(targetId).innerHTML = html;
        console.log(`✅ Carregado com sucesso: ${fileName}`);

        if (fileName === "footer_en.html") {
            console.log("💬 Footer EN carregado — iniciando chatbot loader...");
            loadChatbot();
        }

    } catch (err) {
        console.error("❌ Erro no loadPartial:", err);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("📌 DOM carregado — iniciando loadPartial...");
    loadPartial("header", "header_en.html");
    loadPartial("footer", "footer_en.html");
    
     // ✅ Hero só carrega se existir na página
    if (document.getElementById("hero")) {
        loadPartial("hero", "hero.html");
    }
});


function loadChatbot() {
    console.log("🚀 Iniciando loadChatbot()");

    const script = document.createElement("script");
    script.src = "/static/js/chatbot-loader.js";
    script.defer = true;
    document.body.appendChild(script);

    script.onload = () => console.log("🤖 chatbot-loader.js carregado!");
    script.onerror = () => console.error("❌ Erro ao carregar chatbot-loader.js");

    document.dispatchEvent(new Event("partialsLoaded"));

}





