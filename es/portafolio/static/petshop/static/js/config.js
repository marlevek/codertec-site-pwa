const WHATSAPP = "5541996131762"; // ← só muda aqui no futuro

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("#cta-whatsapp").forEach(btn => {
    btn.href = `https://wa.me/${WHATSAPP}`;
  });
});

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("#cta-whatsapp, #cta-whatsapp-footer").forEach(btn => {
    btn.href = `https://wa.me/${WHATSAPP}`;
  });
});
