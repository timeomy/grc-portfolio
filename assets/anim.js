/* Zabez site: animations + icon initialization
   - initializes Lucide icons (self-hosted, same set as shadcn/ui)
   - scroll-reveal via IntersectionObserver
   - count-up score numbers
   - animates maturity bars on view
   - scroll-parallax on hero decorations
   - idle animations: floating badges, pulsing dots, shimmer buttons
   Usage: <script src="assets/lucide.min.js"></script>
          <script src="assets/anim.js"></script> before </body>
*/
(function () {
  "use strict";

  document.documentElement.classList.add("js");

  /* ---------- lucide icons ---------- */
  function initIcons() {
    if (window.lucide && window.lucide.createIcons) {
      window.lucide.createIcons();
    }
  }

  /* ---------- scroll reveal ---------- */
  function initReveal() {
    var els = document.querySelectorAll(".reveal");
    if (els.length === 0) return;
    if (!("IntersectionObserver" in window)) {
      els.forEach(function (e) { e.classList.add("in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add("in");
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    els.forEach(function (e) { io.observe(e); });
  }

  /* ---------- count-up ---------- */
  function initCountUp() {
    var nums = document.querySelectorAll("[data-count]");
    if (nums.length === 0) return;
    function run(el) {
      var target = parseFloat(el.getAttribute("data-count"));
      var dec = parseInt(el.getAttribute("data-dec") || "0", 10);
      var dur = 1100;
      var start = null;
      function step(ts) {
        if (!start) start = ts;
        var p = Math.min((ts - start) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = (target * eased).toFixed(dec);
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { run(en.target); io.unobserve(en.target); }
      });
    }, { threshold: 0.6 });
    nums.forEach(function (n) { io.observe(n); });
  }

  /* ---------- maturity bars ---------- */
  function initBars() {
    var bars = document.querySelectorAll(".m-fill");
    if (bars.length === 0) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.style.width = en.target.getAttribute("data-w") + "%";
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.4 });
    bars.forEach(function (b) { io.observe(b); });
  }

  /* ---------- scroll parallax on hero decorations ---------- */
  function initParallax() {
    var targets = document.querySelectorAll("[data-parallax]");
    if (targets.length === 0) return;
    var hero = document.querySelector(".hero");
    if (!hero) return;
    function onScroll() {
      var y = window.scrollY;
      if (y > hero.offsetHeight) return;
      targets.forEach(function (t) {
        var speed = parseFloat(t.getAttribute("data-parallax")) || 0.2;
        t.style.transform = "translateY(" + (y * speed) + "px)";
      });
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---------- nav active state ---------- */
  function initNav() {
    var navLinks = document.querySelectorAll(".nav a[href*='#']");
    if (navLinks.length === 0) return;
    var sections = [];
    navLinks.forEach(function (a) {
      var id = a.getAttribute("href").split("#")[1];
      if (id && document.getElementById(id)) {
        sections.push({ id: id, el: document.getElementById(id), link: a });
      }
    });
    if (sections.length === 0) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          sections.forEach(function (s) {
            s.link.style.color = s.id === en.target.id ? "var(--green-dark)" : "";
            s.link.style.background = s.id === en.target.id ? "var(--cream-2)" : "";
          });
        }
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    sections.forEach(function (s) { io.observe(s.el); });
  }

  /* ---------- scroll progress bar ---------- */
  function initProgress() {
    var bar = document.createElement("div");
    bar.className = "progress-bar";
    document.body.appendChild(bar);
    function update() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var p = h > 0 ? (window.scrollY / h) * 100 : 0;
      bar.style.width = p + "%";
    }
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update, { passive: true });
    update();
  }

  /* ---------- magnetic buttons ---------- */
  function initMagnetic() {
    var els = document.querySelectorAll(".magnetic");
    if (els.length === 0 || !window.matchMedia("(hover: hover)").matches) return;
    els.forEach(function (el) {
      el.addEventListener("mousemove", function (e) {
        var r = el.getBoundingClientRect();
        var x = e.clientX - r.left - r.width / 2;
        var y = e.clientY - r.top - r.height / 2;
        el.style.transform = "translate(" + x * 0.15 + "px, " + y * 0.15 + "px)";
      });
      el.addEventListener("mouseleave", function () {
        el.style.transform = "";
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initIcons();
    initReveal();
    initCountUp();
    initBars();
    initParallax();
    initNav();
    initProgress();
    initMagnetic();
  });
})();
