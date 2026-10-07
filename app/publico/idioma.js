'use strict';

/* Conmutador de idioma compartido por todas las pantallas. Cada texto lleva
   sus dos versiones en el propio marcado, asi que cambiar de idioma no pide
   nada al servidor. */

function idioma(l) {
  document.documentElement.lang = l;
  document.querySelectorAll('[data-es]').forEach(function (el) {
    const v = el.getAttribute('data-' + l);
    if (v !== null) el.textContent = v;
  });
  document.querySelectorAll('.idioma button').forEach(function (b) {
    b.classList.toggle('on', b.textContent.trim().toLowerCase() === l);
  });
  try { localStorage.setItem('idioma', l); } catch (e) { /* modo privado */ }
}

try {
  const guardado = localStorage.getItem('idioma');
  if (guardado && guardado !== 'es') idioma(guardado);
} catch (e) { /* sin almacenamiento, se queda en espanol */ }
