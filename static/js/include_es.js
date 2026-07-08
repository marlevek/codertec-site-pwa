// /static/js/include_es.js

console.log("🟡 include_es.js carregado!");

async function loadPartial(targetId, fileName) {
    try {
        const url = `/es/partials/${fileName}`;
        console.log(`🔹 Tentando carregar: ${url}`);

        const response = await fetch(url);
        console.log("📡 Status:", response.status);

        if (!response.ok) throw new Error(`Falha ao carregar ${url}`);

        const html = await response.text();
        document.getElementById(targetId).innerHTML = html;
        console.log(`✅ Carregado com sucesso: ${fileName}`);

        if (fileName === "footer_es.html") {
            console.log("💬 Footer ES carregado — iniciando chatbot loader...");
            loadChatbot();
        }

    } catch (err) {
        console.error("❌ Erro no loadPartial:", err);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("📌 DOM carregado — iniciando loadPartial...");
    loadPartial("header", "header_es.html");
    loadPartial("footer", "footer_es.html");

    // ✅ Hero só carrega se existir na página
    if (document.getElementById("hero")) {
        loadPartial("hero", "hero.html");
    }
});

function loadChatbot() {
    // Widget AtendeSite (substitui o chatbot antigo). createElement para o
    // <script> de fato executar.
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
