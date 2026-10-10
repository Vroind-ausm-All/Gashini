/* Läuft vor dem ersten Rendern: markiert JavaScript und erlaubte Bewegung. Speichert nichts. */
(function (h) {
  h.classList.add('js');
  try { if (window.matchMedia('(prefers-reduced-motion: no-preference)').matches) h.classList.add('bewegung'); } catch (e) {}
})(document.documentElement);
