/* Artisan Robin : menu, diaporama, visionneuse photo, avant/après, avis, filtres, estimateur et formulaires de devis. */
(function () {
  "use strict";

  var PHONE = "+33666553562";
  var WHATSAPP = "33666553562";
  var doc = document;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function $(s, r) { return (r || doc).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); }
  function fmt(v) {
    v = Math.round(v / 100) * 100;
    return v.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + " €";
  }

  // Menu mobile
  var header = $("[data-header]");
  var toggle = $(".menu-btn");
  function setMenu(open) {
    header.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
    doc.body.classList.toggle("no-scroll", open);
  }
  if (header && toggle) {
    toggle.addEventListener("click", function () { setMenu(!header.classList.contains("open")); });
    window.matchMedia("(min-width: 1101px)").addEventListener("change", function (m) { if (m.matches) setMenu(false); });
    $$(".nav a").forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
  }

  // Sous-menu : fermeture au clic extérieur et avec Échap
  var subs = $$(".sub");
  doc.addEventListener("click", function (e) {
    if (window.innerWidth <= 1100) return;
    subs.forEach(function (d) { if (d.open && !d.contains(e.target)) d.open = false; });
  });
  doc.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    subs.forEach(function (d) { if (d.open) { d.open = false; $("summary", d).focus(); } });
    if (header && header.classList.contains("open")) { setMenu(false); toggle.focus(); }
  });

  // En-tête et barre d'appel au défilement
  var callbar = $("[data-callbar]");
  var tick = false;
  function onScroll() {
    if (tick) return;
    tick = true;
    window.requestAnimationFrame(function () {
      var y = window.scrollY || window.pageYOffset;
      if (callbar) callbar.classList.toggle("show", y > 480);
      if (header) header.classList.toggle("solid", y > 10);
      tick = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Diaporama du héros
  var slides = $$("[data-slides] .hs");
  if (slides.length > 1 && !reduce) {
    var cur = 0;
    setInterval(function () {
      slides[cur].classList.remove("is-on");
      cur = (cur + 1) % slides.length;
      slides[cur].classList.add("is-on");
    }, 6500);
  }

  // Apparition au défilement
  if ("IntersectionObserver" in window && !reduce) {
    var targets = $$(".sec-head, .metiers, .cards, .gal, .steps, .split, .zones-grid, .tms, .ba, .values, .posts, .art-sec, .devis-grid, .band-in");
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    targets.forEach(function (t) {
      var r = t.getBoundingClientRect();
      if (r.top > window.innerHeight) { t.classList.add("rv"); io.observe(t); }
    });
  }

  // Visionneuse photo
  var box = $("[data-lightbox]");
  var links = $$("a[data-lb]");
  if (box && links.length) {
    var bimg = $("img", box), bcap = $("figcaption", box), idx = 0, last = null;
    var visible = function () { return links.filter(function (a) { return !a.closest("[hidden]"); }); };
    var show = function (i) {
      var list = visible();
      idx = (i + list.length) % list.length;
      var a = list[idx];
      bimg.src = a.getAttribute("href");
      bimg.alt = a.getAttribute("data-cap") || "";
      bcap.textContent = a.getAttribute("data-cap") || "";
    };
    var open = function (a) {
      last = a;
      show(visible().indexOf(a));
      box.hidden = false;
      doc.body.classList.add("no-scroll");
      $(".lb-x", box).focus();
    };
    var close = function () {
      box.hidden = true;
      doc.body.classList.remove("no-scroll");
      bimg.removeAttribute("src");
      if (last) last.focus();
    };
    links.forEach(function (a) { a.addEventListener("click", function (e) { e.preventDefault(); open(a); }); });
    $(".lb-x", box).addEventListener("click", close);
    $(".lb-p", box).addEventListener("click", function () { show(idx - 1); });
    $(".lb-n", box).addEventListener("click", function () { show(idx + 1); });
    box.addEventListener("click", function (e) { if (e.target === box) close(); });
    doc.addEventListener("keydown", function (e) {
      if (box.hidden) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "ArrowRight") show(idx + 1);
    });
    var x0 = null;
    box.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    box.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
      x0 = null;
    });
  }

  // Avant / après
  $$("[data-ba]").forEach(function (f) {
    var r = $("input", f);
    r.addEventListener("input", function () { f.style.setProperty("--pos", r.value + "%"); });
  });

  // Avis : défilement
  $$("[data-tms]").forEach(function (t) {
    var track = $(".tms-track", t);
    var step = function (d) { track.scrollBy({ left: d * (track.clientWidth * 0.9), behavior: reduce ? "auto" : "smooth" }); };
    $(".tms-p", t).addEventListener("click", function () { step(-1); });
    $(".tms-n", t).addEventListener("click", function () { step(1); });
  });

  // Filtres (réalisations, articles)
  $$(".filters").forEach(function (f) {
    var list = f.parentNode.querySelector("[data-gal]");
    if (!list) return;
    $$("button", f).forEach(function (b) {
      b.addEventListener("click", function () {
        var v = b.getAttribute("data-f");
        $$("button", f).forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
        $$(":scope > li", list).forEach(function (li) {
          li.hidden = !(v === "*" || (" " + li.getAttribute("data-tags") + " ").indexOf(" " + v + " ") > -1);
        });
      });
    });
  });

  // Estimateur
  var est = $("[data-estim]");
  if (est) {
    var sel = $("select", est), range = $("input[type=range]", est), outS = $("[data-surf]", est), out = $("[data-out]", est);
    var calc = function () {
      var o = sel.options[sel.selectedIndex], s = Number(range.value);
      outS.textContent = s + " m²";
      out.textContent = fmt(Number(o.getAttribute("data-min")) * s) + " à " + fmt(Number(o.getAttribute("data-max")) * s);
    };
    est.addEventListener("input", calc);
    est.addEventListener("change", calc);
    calc();
  }

  // Formulaires de devis
  function el(tag, attrs, text) {
    var n = doc.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    if (text) n.textContent = text;
    return n;
  }
  $$("form[data-devis]").forEach(function (form) {
    var status = $(".form-status", form);
    function show(kind, nodes) {
      status.className = "form-status " + kind;
      status.textContent = "";
      nodes.forEach(function (n) { status.appendChild(n); });
      status.setAttribute("tabindex", "-1");
      status.focus();
    }
    function summary(d) {
      return "Demande de devis (site couvreur-thorignysurmarne.fr)\n" +
        "Nom : " + d.nom + "\nTéléphone : " + d.telephone + "\n" +
        (d.email ? "Email : " + d.email + "\n" : "") +
        "Commune : " + d.commune + "\nTravaux : " + d.type + "\nRappel : " + d.rappel + "\n\n" + d.message;
    }
    function fallback(d) {
      var text = summary(d);
      var actions = el("div", { "class": "fallback-actions" });
      actions.appendChild(el("a", { "class": "btn btn-red", href: "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(text), rel: "noopener" }, "Envoyer sur WhatsApp"));
      actions.appendChild(el("a", { "class": "btn btn-line", href: "sms:" + PHONE + "?&body=" + encodeURIComponent(text) }, "Envoyer par SMS"));
      actions.appendChild(el("a", { "class": "btn btn-line", href: "tel:" + PHONE }, "Appeler"));
      show("err", [el("p", {}, "L'envoi par le site n'a pas abouti. Votre demande est prête : envoyez-la par WhatsApp ou par SMS, ou appelez-nous."), actions]);
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var first = null;
      $$("[required]", form).forEach(function (f) {
        var ok = f.type === "checkbox" ? f.checked : f.value.trim() !== "" && f.checkValidity();
        f.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok && !first) first = f;
      });
      if (first) {
        show("err", [el("p", {}, "Complétez les champs signalés en rouge.")]);
        first.focus();
        return;
      }
      var rap = $("input[name=rappel]:checked", form);
      var d = {
        nom: form.elements.nom.value.trim(),
        telephone: form.elements.telephone.value.trim(),
        email: form.elements.email ? form.elements.email.value.trim() : "",
        commune: form.elements.commune.value.trim(),
        type: form.elements.type.value,
        message: form.elements.message.value.trim(),
        rappel: rap ? rap.value : "Indifférent",
        site_web: form.elements.site_web.value,
        consentement: form.elements.consentement.checked,
        page: location.pathname
      };
      var button = $("button[type=submit]", form);
      var label = $("span", button);
      var txt = label.textContent;
      button.disabled = true;
      label.textContent = "Envoi en cours…";
      fetch("/api/devis", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(d) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { status: r.status, body: j }; }); })
        .then(function (res) {
          if (res.status === 200 && res.body.ok) {
            form.reset();
            show("ok", [el("p", {}, "Demande envoyée. Nous vous rappelons très vite pour convenir d'une visite.")]);
          } else if (res.status === 400 && res.body.error) {
            show("err", [el("p", {}, res.body.error)]);
          } else {
            fallback(d);
          }
        })
        .catch(function () { fallback(d); })
        .then(function () { button.disabled = false; label.textContent = txt; });
    });
  });
})();
