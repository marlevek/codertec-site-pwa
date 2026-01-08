let deferredPrompt = null;

document.addEventListener("partialsLoaded", () => {
    const installBtn = document.getElementById("installAppBtn");

    if (!installBtn) return;

    // Esconde se já estiver em modo app
    if (window.matchMedia("(display-mode: standalone)").matches) {
        installBtn.style.display = "none";
        return;
    }

    // Sempre mostra o botão
    installBtn.style.display = "inline-block";

    // Captura o evento se o Chrome liberar
    window.addEventListener("beforeinstallprompt", (e) => {
        e.preventDefault();
        deferredPrompt = e;
    });

    installBtn.addEventListener("click", async () => {
        // Se o Chrome liberou o prompt
        if (deferredPrompt) {
            deferredPrompt.prompt();
            await deferredPrompt.userChoice;
            deferredPrompt = null;
            installBtn.style.display = "none";
            return;
        }

        // Fallback universal (Chrome/iOS)
        alert(
            "Para instalar o aplicativo:\n\n" +
            "• Android/Chrome: menu ⋮ → Instalar app\n" +
            "• iPhone/Safari: compartilhar → Adicionar à Tela de Início"
        );
    });
});

