let deferredPrompt = null;

document.addEventListener("partialsLoaded", () => {
    const installBtn = document.getElementById("installAppBtn");
    if (!installBtn) return;

    // Esconde por padrão
    installBtn.style.display = "none";

    // Se já estiver instalado como app
    if (window.matchMedia("(display-mode: standalone)").matches) {
        return;
    }

    // Captura o evento APENAS quando o navegador permitir
    window.addEventListener("beforeinstallprompt", (e) => {
        e.preventDefault();
        deferredPrompt = e;

        // Só agora mostra o botão
        installBtn.style.display = "inline-block";
    });

    installBtn.addEventListener("click", async () => {
        if (!deferredPrompt) {
            // Fallback universal
            alert(
                "Para instalar o aplicativo:\n\n" +
                "• Android/Chrome: menu ⋮ → Instalar app\n" +
                "• iPhone/Safari: compartilhar → Adicionar à Tela de Início"
            );
            return;
        }

        deferredPrompt.prompt();
        await deferredPrompt.userChoice;
        deferredPrompt = null;
        installBtn.style.display = "none";
    });
});
