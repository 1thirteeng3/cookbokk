// Seletor de idioma aponta para a MESMA página no outro idioma (pt em /, en em /en/).
// Language selector points to the SAME page in the other language.
(function () {
  function relink() {
    var path = location.pathname;
    var isEn = path === "/en/" || path.indexOf("/en/") === 0;
    var base = isEn ? path.slice(3) || "/" : path;
    document.querySelectorAll("a.md-select__link[hreflang]").forEach(function (a) {
      var lang = a.getAttribute("hreflang");
      if (lang === "en") a.setAttribute("href", "/en" + base + location.hash);
      if (lang === "pt") a.setAttribute("href", base + location.hash);
    });
  }
  if (typeof document$ !== "undefined") document$.subscribe(relink);
  else document.addEventListener("DOMContentLoaded", relink);
})();
