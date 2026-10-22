(function () {
  var root = document.documentElement;

  // Preview-only design switcher. Remembers the choice per browser so it carries across pages.
  var STYLES = { d: "Shop Blue", a: "Shop Ticket", b: "Showroom", c: "Blueprint" };
  function setStyle(s, remember) {
    if (!STYLES[s]) s = "d";
    root.setAttribute("data-style", s);
    document.querySelectorAll(".switcher button").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.style === s)); });
    if (remember) { try { localStorage.setItem("na-style-v3", s); } catch (e) {} }
  }
  var start = "d";
  try { start = localStorage.getItem("na-style-v3") || "d"; } catch (e) {}
  var hash = (location.hash || "").replace("#", "");
  if (/^style-[abcd]$/.test(hash)) start = hash.slice(6);
  setStyle(start, false);
  document.querySelectorAll(".switcher button").forEach(function (b) {
    b.addEventListener("click", function () { setStyle(b.dataset.style, true); });
  });

  // Mobile menu
  var menuBtn = document.getElementById("menu-btn"), menu = document.getElementById("mobile-nav");
  if (menuBtn && menu) {
    menuBtn.addEventListener("click", function () {
      var open = menu.hidden;
      menu.hidden = !open;
      menuBtn.setAttribute("aria-expanded", String(open));
      menuBtn.querySelector(".txt").textContent = open ? "Close" : "Menu";
    });
  }

  // Open / closed, in Chicago time. [open, close] in minutes after midnight, Sunday first.
  var HOURS = [[480, 780], [420, 1080], [420, 1080], [420, 1080], [420, 1080], [420, 1080], [420, 1080]];
  var DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  function fmt(m) { var h = Math.floor(m / 60), mm = m % 60, ap = h >= 12 ? "pm" : "am"; h = h % 12 || 12; return h + (mm ? ":" + String(mm).padStart(2, "0") : "") + ap; }
  try {
    var parts = new Intl.DateTimeFormat("en-US", { timeZone: "America/Chicago", weekday: "short", hour: "numeric", minute: "numeric", hourCycle: "h23" }).formatToParts(new Date());
    var get = function (t) { var p = parts.find(function (x) { return x.type === t; }); return p ? p.value : ""; };
    var day = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(get("weekday"));
    var mins = parseInt(get("hour"), 10) * 60 + parseInt(get("minute"), 10);
    if (day >= 0 && !isNaN(mins)) {
      var h = HOURS[day], open = mins >= h[0] && mins < h[1], msg;
      if (open) msg = "Open now · closes " + fmt(h[1]);
      else if (mins < h[0]) msg = "Closed · opens today at " + fmt(h[0]);
      else { var nd = (day + 1) % 7; msg = "Closed · opens " + DAYS[nd] + " at " + fmt(HOURS[nd][0]); }
      document.querySelectorAll("[data-open-text]").forEach(function (el) { el.textContent = msg; });
      document.querySelectorAll("[data-open-dot]").forEach(function (el) { el.classList.add(open ? "is-open" : "is-closed"); });
      var row = document.querySelector('.hours tr[data-day="' + day + '"]');
      if (row) row.classList.add("today");
    }
  } catch (e) {}

  // Copy phone number
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    var label = btn.textContent;
    btn.addEventListener("click", function () {
      var done = function () { btn.textContent = "Copied"; setTimeout(function () { btn.textContent = label; }, 1800); };
      var fallback = function () { var t = document.getElementById(btn.dataset.copy); var r = document.createRange(); r.selectNodeContents(t); var s = getSelection(); s.removeAllRanges(); s.addRange(r); btn.textContent = "Selected, press Ctrl+C"; };
      try { navigator.clipboard.writeText(document.getElementById(btn.dataset.copy).textContent.trim()).then(done, fallback); } catch (e) { fallback(); }
    });
  });

  // Service filters
  var chips = document.querySelectorAll(".chip[data-filter]");
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var f = chip.dataset.filter;
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c === chip)); });
      document.querySelectorAll(".svc[data-cat]").forEach(function (card) {
        var show = f === "all" || card.dataset.cat === f;
        card.classList.remove("is-showing");
        card.classList.toggle("is-hiding", !show);
        if (show) { void card.offsetWidth; card.classList.add("is-showing"); }
      });
    });
  });

  // Count the rating up once it scrolls into view. The resting text is already the real number.
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce && "IntersectionObserver" in window) {
    document.querySelectorAll("[data-count]").forEach(function (el) {
      var target = parseFloat(el.dataset.count), dec = (el.dataset.count.split(".")[1] || "").length;
      var io = new IntersectionObserver(function (entries) {
        if (!entries[0].isIntersecting) return;
        io.disconnect();
        var t0 = performance.now(), dur = 1100;
        (function tick(now) {
          var p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3);
          el.textContent = (target * e).toFixed(dec);
          if (p < 1) requestAnimationFrame(tick); else el.textContent = el.dataset.count;
        })(t0);
      }, { threshold: 0.6 });
      io.observe(el);
    });
  }

  // Appointment request form. The hosted site will post it to the shop's inbox;
  // until that's connected, it validates and says plainly that nothing was sent.
  var form = document.getElementById("request-form");
  if (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var status = document.getElementById("rf-status"), bad = null;
      ["rf-name", "rf-phone"].forEach(function (id) {
        var el = document.getElementById(id), ok = el.value.trim().length > 1;
        el.setAttribute("aria-invalid", String(!ok));
        if (!ok && !bad) bad = el;
      });
      if (bad) { status.className = "form-note is-error"; status.textContent = "Add your name and phone number so the shop can call you back."; bad.focus(); return; }
      status.className = "form-note is-done";
      status.textContent = "Preview only: this request wasn't sent. Once the site is live it goes straight to the shop.";
    });
  }

  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
