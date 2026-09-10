const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#main-nav');
function closeMenu() {
  toggle.setAttribute('aria-expanded', 'false');
  nav.classList.remove('is-open');
}
toggle.hidden = false;
toggle.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('is-open', open);
});
nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && nav.classList.contains('is-open')) { closeMenu(); toggle.focus(); }
});
document.addEventListener('click', event => {
  if (!nav.contains(event.target) && !toggle.contains(event.target)) closeMenu();
});
const dialog = document.querySelector('#call-dialog');
document.querySelectorAll('[data-demo-call]').forEach(link => {
  link.addEventListener('click', event => { event.preventDefault(); dialog.showModal(); });
});
document.querySelector('#close-call').addEventListener('click', () => dialog.close());
const form = document.querySelector('#quote-form');
document.querySelector('#submit-quote').disabled = false;
form.addEventListener('submit', event => {
  event.preventDefault();
  document.querySelector('#form-status').textContent = 'Demo complete. No request was sent and your details have not been saved. This is a concept website, not a service booking.';
  form.reset();
  document.querySelector('#form-status').focus();
});
document.querySelectorAll('[data-service]').forEach(link => {
  link.addEventListener('click', () => { document.querySelector('#service').value = link.dataset.service; });
});
