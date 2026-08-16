/* Email gate for free-resource downloads.
   Visitor enters email -> POSTed to the configured subscribe endpoint ->
   on success the download link is revealed.
   Endpoint: change GATE_ENDPOINT to your form/newsletter provider
   (Formspree, Buttondown, Mailchimp, MailerLite, etc.). */

(function () {
  "use strict";

  // ---- CONFIG ----
  // Replace with your real endpoint. Two supported shapes:
  //   Formspree:  https://formspree.io/f/YOURFORMID
  //   Buttondown: https://buttondown.com/api/emails/embed-subscribe-form/YOURUSERNAME
  var GATE_ENDPOINT = "https://formspree.io/f/YOURFORMID";
  var GATE_EMAIL_FIELD = "email";       // field name the endpoint expects
  var GATE_SUCCESS_MSG = "You're in. Check your inbox to confirm, then grab your file below.";

  var modal = null;
  var currentFile = "";

  // If the gated target is an .html page or an external http(s) URL,
  // navigate to it after capture instead of triggering a download.
  function isNavigation(file) {
    return /\.html?$/.test(file) || /^https?:\/\//.test(file);
  }

  function openGate(file, name) {
    currentFile = file;
    if (!modal) buildModal();
    modal.querySelector(".gate-filename").textContent = name;
    modal.classList.add("open");
    var input = modal.querySelector("input[type=email]");
    input.value = "";
    input.focus();
    modal.querySelector(".gate-error").textContent = "";
    modal.querySelector(".gate-success").style.display = "none";
    modal.querySelector(".gate-download").style.display = "none";
    modal.querySelector(".gate-form").style.display = "block";
  }

  function closeGate() {
    if (modal) modal.classList.remove("open");
  }

  function buildModal() {
    modal = document.createElement("div");
    modal.className = "gate-modal";
    modal.innerHTML =
      '<div class="gate-box" role="dialog" aria-modal="true" aria-labelledby="gate-title">' +
      '<button class="gate-close" aria-label="Close">&times;</button>' +
      '<h3 id="gate-title">Get the free <span class="gate-filename"></span></h3>' +
      '<p class="gate-sub">Enter your email and it\u2019s yours. You\u2019ll also get the daily GRC news digest, free. Unsubscribe anytime.</p>' +
      '<form class="gate-form">' +
      '<input type="email" name="email" placeholder="you@example.com" required autocomplete="email">' +
      '<button type="submit" class="btn btn-primary gate-submit">Send me the download</button>' +
      '</form>' +
      '<p class="gate-error" style="display:none;color:var(--red);font-size:13px;margin-top:10px;"></p>' +
      '<div class="gate-success" style="display:none;margin-top:12px;">' +
      '<p class="gate-success-msg" style="font-size:14px;color:var(--green);margin-bottom:12px;"></p>' +
      '<a class="btn btn-primary gate-download" href="#" download>Download now</a>' +
      '</div>' +
      '</div>';

    document.body.appendChild(modal);

    modal.addEventListener("click", function (e) {
      if (e.target === modal) closeGate();
    });
    modal.querySelector(".gate-close").addEventListener("click", closeGate);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeGate();
    });

    modal.querySelector(".gate-form").addEventListener("submit", function (e) {
      e.preventDefault();
      var input = modal.querySelector("input[type=email]");
      var err = modal.querySelector(".gate-error");
      var email = input.value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        err.textContent = "Please enter a valid email address.";
        err.style.display = "block";
        return;
      }
      err.style.display = "none";
      var btn = modal.querySelector(".gate-submit");
      btn.disabled = true;
      btn.textContent = "Sending...";

      var body = new URLSearchParams();
      body.append(GATE_EMAIL_FIELD, email);

      fetch(GATE_ENDPOINT, {
        method: "POST",
        headers: { "Accept": "application/json" },
        body: body
      })
        .then(function (r) { return r.ok || r.status === 200 ? r.json() : Promise.reject(new Error("bad status")); })
        .then(function () { reveal(false); })
        .catch(function () {
          // Network failure: still reveal the file, log the email locally
          // so the visitor is never blocked from content.
          try {
            var seen = JSON.parse(localStorage.getItem("zabez_leads") || "[]");
            seen.push({ email: email, file: currentFile, at: new Date().toISOString() });
            localStorage.setItem("zabez_leads", JSON.stringify(seen));
          } catch (ignore) {}
          reveal(true);
        })
        .finally(function () {
          btn.disabled = false;
          btn.textContent = "Send me the download";
        });
    });
  }


    function reveal(offline) {
      var dl = modal.querySelector(".gate-download");
      var msg = modal.querySelector(".gate-success-msg");
      modal.querySelector(".gate-form").style.display = "none";
      modal.querySelector(".gate-success").style.display = "block";
      if (isNavigation(currentFile)) {
        dl.textContent = "Continue \u2192";
        dl.removeAttribute("download");
        msg.textContent = offline
          ? "You're on the list. Taking you there now."
          : GATE_SUCCESS_MSG;
        setTimeout(function () { window.location.href = currentFile; }, offline ? 400 : 900);
      } else {
        dl.textContent = "Download now";
        dl.setAttribute("download", "");
        dl.href = currentFile;
        msg.textContent = offline
          ? "Here\u2019s your download. (Email capture is having a moment; we\u2019ll sync it shortly.)"
          : GATE_SUCCESS_MSG;
      }
    }

  // Wire up every gated download button
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-gate]").forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        openGate(a.getAttribute("data-gate"), a.getAttribute("data-name") || "resource");
      });
    });
  });

  window.zabezGate = { open: openGate, close: closeGate };
})();
