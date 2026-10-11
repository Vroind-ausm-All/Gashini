/* Läuft vor dem ersten Rendern: markiert JavaScript und erlaubte Bewegung. Speichert nichts. */
(function (h) {
  h.classList.add('js');
  try { if (window.matchMedia('(prefers-reduced-motion: no-preference)').matches) h.classList.add('bewegung'); } catch (e) {}
  // Jede Seite beginnt oben – auch beim Zurück/Vor im Browser und beim Neuladen. Der Browser stellt die alte
  // Scroll-Position sonst wieder her. Sprungmarken (#anfrage, #wandaufbau …) behalten ihr Ziel (site.js).
  try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch (e) {}
})(document.documentElement);
