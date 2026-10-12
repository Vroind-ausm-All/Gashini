/* Läuft vor dem ersten Rendern: markiert JavaScript und erlaubte Bewegung. Speichert nichts. */
(function (h) {
  h.classList.add('js');
  try { if (window.matchMedia('(prefers-reduced-motion: no-preference)').matches) h.classList.add('bewegung'); } catch (e) {}
  // Jede Seite beginnt oben – auch beim Zurück/Vor im Browser und beim Neuladen. Der Browser stellt die alte
  // Scroll-Position sonst wieder her. Sprungmarken (#anfrage, #wandaufbau …) behalten ihr Ziel (site.js).
  try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch (e) {}
  // Vorschau: Kundenansicht schon vor dem ersten Bild setzen, damit Redaktionshinweise nicht aufblitzen
  // (Schalter und ?ansicht=kunde|intern: site.js)
  try {
    var q = window.location.search;
    if (/[?&]ansicht=kunde\b/.test(q) || (!/[?&]ansicht=intern\b/.test(q) && window.localStorage.getItem('gashini-kundenansicht') === '1')) h.classList.add('kundenansicht');
  } catch (e) {}
})(document.documentElement);
