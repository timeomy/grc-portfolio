/* Zabez course checkout — Billplz flow (self-contained)
   Clicking an "Enroll" button opens a small email-capture modal, posts to
   the Cloudflare Worker, which creates a Billplz bill. The buyer is then
   redirected to Billplz's hosted payment page.

   SETUP: put your deployed worker URL below.
*/
(function () {
  "use strict";

  var CHECKOUT_ENDPOINT = "https://YOUR-WORKER.workers.dev/api/checkout";

  var modal = null;

  function ensureModal() {
    if (modal) return modal;
    modal = document.createElement("div");
    modal.className = "gate-modal checkout-modal";
    modal.innerHTML =
      '<div class="gate-box">' +
      '<button type="button" class="gate-close" aria-label="Close">&times;</button>' +
      '<div class="gate-icon"><i data-lucide="lock"></i></div>' +
      '<h3 class="gate-title">Enroll in the GRC Analyst Program</h3>' +
      '<p class="gate-sub">RM 149 · lifetime access · 14-day refund. Enter your email to start checkout.</p>' +
      '<form class="gate-form">' +
      '<input type="email" name="email" placeholder="you@example.com" required autocomplete="email">' +
      '<button type="submit" class="btn btn-primary" style="width:100%;justify-content:center;">Proceed to payment →</button>' +
      '</form>' +
      '<p class="gate-fine">Payments handled securely by Billplz. No account needed.</p>' +
      '</div>';
    document.body.appendChild(modal);

    // wire close + submit
    modal.querySelector(".gate-close").addEventListener("click", function () {
      modal.classList.remove("open");
    });
    modal.addEventListener("click", function (e) {
      if (e.target === modal) modal.classList.remove("open");
    });
    modal.querySelector(".gate-form").addEventListener("submit", function (e) {
      e.preventDefault();
      var email = (modal.querySelector('input[type="email"]').value || "").trim();
      if (!email || !/.+@.+\..+/.test(email)) {
        modal.querySelector('input[type="email"]').focus();
        return;
      }
      var btn = modal.querySelector('button[type="submit"]');
      btn.disabled = true;
      btn.textContent = "Creating your payment…";
      fetch(CHECKOUT_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email }),
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.payment_url) {
            window.location.href = data.payment_url;
          } else {
            alert(data.error || "Checkout failed. Please try again.");
            btn.disabled = false;
            btn.textContent = "Proceed to payment →";
          }
        })
        .catch(function () {
          alert("Could not reach the payment service. Please try again or email hi@zabez.com.");
          btn.disabled = false;
          btn.textContent = "Proceed to payment →";
        });
    });
    return modal;
  }

  function openCheckout() {
    var m = ensureModal();
    m.classList.add("open");
    // render lucide icons inside the freshly created modal
    if (window.lucide && window.lucide.createIcons) {
      window.lucide.createIcons({ attrs: { class: ["lucide"] } });
    }
    var emailInput = m.querySelector('input[type="email"]');
    if (emailInput) setTimeout(function () { emailInput.focus(); }, 50);
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-checkout]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        openCheckout();
      });
    });
  });

  window.zabezCheckout = { open: openCheckout };
})();
