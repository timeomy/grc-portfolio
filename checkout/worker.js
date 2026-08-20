/**
 * Zabez GRC worker: course checkout + email-gate leads + admin console.
 *
 * Routes:
 *   POST /api/subscribe  — email gate capture (stores lead in LEADS KV)
 *   GET  /api/leads      — JSON export, Authorization: Bearer <LEADS_EXPORT_TOKEN>
 *   POST /api/checkout   — creates a Billplz bill for the GRC Analyst Program
 *   GET  /admin          — leads dashboard (HTML shell, data loads via /api/leads)
 *
 * SETUP:
 *  1. wrangler secret put BILLPLZ_API_KEY
 *  2. wrangler secret put BILLPLZ_COLLECTION_ID
 *  3. wrangler secret put LEADS_EXPORT_TOKEN
 *  4. wrangler deploy
 */

const PRICE_SEN = 499 * 100; // RM 499
const DESCRIPTION = "GRC Analyst Program | lifetime access";
const CALLBACK_URL = "https://zabez.com/courses/thanks.html"; // server notification
const REDIRECT_URL = "https://zabez.com/courses/thanks.html"; // buyer lands here after paying
const REFERENCE_LABEL = "Order";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders() });
    }

    if (request.method === "POST" && url.pathname === "/api/subscribe") {
      return handleSubscribe(request, env);
    }
    if (request.method === "GET" && url.pathname === "/api/leads") {
      return handleLeadsExport(request, env);
    }
    if (request.method === "POST" && url.pathname === "/api/checkout") {
      return handleCheckout(request, env);
    }
    if (request.method === "GET" && (url.pathname === "/admin" || url.pathname === "/admin/")) {
      return new Response(ADMIN_HTML, {
        headers: { "Content-Type": "text/html; charset=utf-8" },
      });
    }

    return json({ error: "Not found" }, 404);
  },
};

// Email gate: capture a lead, store it in KV, reveal the download.
// Accepts form-encoded or JSON. Requires the LEADS KV binding.
async function handleSubscribe(request, env) {
  try {
    const contentType = request.headers.get("Content-Type") || "";
    let email = "";
    let file = "";
    if (contentType.includes("application/json")) {
      const body = await request.json();
      email = (body.email || "").trim().toLowerCase();
      file = (body.file || "").trim();
    } else {
      const form = await request.formData();
      email = String(form.get("email") || "").trim().toLowerCase();
      file = String(form.get("file") || "").trim();
    }

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 254) {
      return json({ error: "A valid email is required." }, 400);
    }

    const existing = await env.LEADS.get(email, { type: "json" });
    const record = {
      email,
      files: existing ? [...new Set([...(existing.files || []), file].filter(Boolean))] : [file].filter(Boolean),
      first_seen: existing ? existing.first_seen : new Date().toISOString(),
      last_seen: new Date().toISOString(),
      count: existing ? (existing.count || 1) + 1 : 1,
    };
    await env.LEADS.put(email, JSON.stringify(record));

    return json({ ok: true });
  } catch (err) {
    return json({ error: "Subscribe failed. Please try again." }, 500);
  }
}

// Lead export: GET /api/leads with Authorization: Bearer <LEADS_EXPORT_TOKEN>
async function handleLeadsExport(request, env) {
  const auth = request.headers.get("Authorization") || "";
  if (!env.LEADS_EXPORT_TOKEN || auth !== "Bearer " + env.LEADS_EXPORT_TOKEN) {
    return json({ error: "Unauthorized" }, 401);
  }
  const leads = [];
  let cursor;
  do {
    const page = await env.LEADS.list({ cursor });
    for (const key of page.keys) {
      const value = await env.LEADS.get(key.name, { type: "json" });
      if (value) leads.push(value);
    }
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);
  return json({ count: leads.length, leads });
}

async function handleCheckout(request, env) {
  try {
    const body = await request.json();
    const email = (body.email || "").trim();
    const name = (body.name || "GRC Program Student").trim();

    if (!email || !/.+@.+\..+/.test(email)) {
      return json({ error: "A valid email is required." }, 400);
    }

    // Create the bill at Billplz
    const form = new URLSearchParams();
    form.set("collection_id", env.BILLPLZ_COLLECTION_ID);
    form.set("email", email);
    form.set("name", name);
    form.set("amount", String(PRICE_SEN));
    form.set("description", DESCRIPTION);
    form.set("callback_url", CALLBACK_URL);
    form.set("redirect_url", REDIRECT_URL);
    form.set("reference_1_label", REFERENCE_LABEL);
    form.set("reference_1", "GRC-ANALYST-PROGRAM");

    const billRes = await fetch("https://www.billplz.com/api/v3/bills", {
      method: "POST",
      headers: {
        "Authorization": "Basic " + btoa(env.BILLPLZ_API_KEY + ":"),
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: form,
    });
    const bill = await billRes.json();
    if (!billRes.ok || !bill.url) {
      return json(
        { error: "Payment provider error. Please try again or email hi@zabez.com.", detail: bill.error || bill },
        502
      );
    }

    // Return the Billplz-hosted payment URL; frontend redirects the buyer
    return json({ payment_url: bill.url, bill_id: bill.id });
  } catch (err) {
    return json({ error: "Checkout failed. Please try again." }, 500);
  }
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...corsHeaders(),
    },
  });
}

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
  };
}

/* ============================================================
   /admin — leads console.
   Static shell with no data baked in; the browser fetches
   /api/leads with the export token the owner pastes once
   (kept in localStorage). Sending uses Gmail compose links,
   so mails go out from the owner's own inbox and replies
   come back to it.
   ============================================================ */

const ADMIN_HTML = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>ZABEZ Leads Console</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --primary: #1C1CE2; --primary-hover: #1414A8; --primary-tint: #EBEBFF;
    --text: #16161F; --dim: #4C4C59; --faint: #8B8BA0;
    --line: #E2E2F0; --cream: #F7F7FD;
    --wash: radial-gradient(42% 60% at 12% 10%, rgba(127,127,213,.18) 0%, transparent 100%),
            radial-gradient(46% 62% at 88% 6%, rgba(134,168,231,.2) 0%, transparent 100%),
            #FFFFFF;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: "Inter", -apple-system, sans-serif; background: var(--wash); color: var(--text); font-size: 15px; line-height: 1.55; min-height: 100vh; }
  .wrap { max-width: 1100px; margin: 0 auto; padding: 40px 24px 80px; }
  h1 { font-size: 28px; font-weight: 800; letter-spacing: -0.02em; }
  h1 .dot { color: var(--primary); }
  .sub { color: var(--dim); margin-top: 4px; }
  .card { background: #fff; border: 1px solid var(--line); border-radius: 16px; box-shadow: 0 4px 17px rgba(22,22,31,.06); padding: 22px; margin-top: 22px; }
  .row { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
  input[type=password], input[type=search] { font: inherit; padding: 10px 14px; border: 1px solid var(--line); border-radius: 10px; outline: none; min-width: 260px; }
  input:focus { border-color: var(--primary); }
  button, .btn { font: inherit; font-weight: 600; padding: 10px 18px; border-radius: 10px; border: 1px solid var(--primary); cursor: pointer; background: var(--primary); color: #fff; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; }
  button:hover, .btn:hover { background: var(--primary-hover); }
  button.ghost { background: #fff; color: var(--primary); }
  button.ghost:hover { background: var(--primary-tint); }
  button:disabled { opacity: .45; cursor: default; }
  .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; margin-top: 22px; }
  .stat { background: #fff; border: 1px solid var(--line); border-radius: 14px; padding: 16px 18px; }
  .stat b { display: block; font-size: 26px; font-weight: 800; color: var(--primary); }
  .stat span { font-size: 12.5px; color: var(--dim); font-weight: 500; }
  table { width: 100%; border-collapse: collapse; margin-top: 6px; }
  th { text-align: left; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .06em; color: var(--faint); padding: 10px 10px; border-bottom: 2px solid var(--primary); white-space: nowrap; }
  td { padding: 12px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
  tr:hover td { background: var(--cream); }
  .email { font-weight: 600; }
  .chip { display: inline-block; font-size: 11.5px; font-weight: 500; background: var(--cream); border: 1px solid var(--line); border-radius: 999px; padding: 2px 10px; margin: 2px 4px 2px 0; color: var(--dim); white-space: nowrap; }
  .muted { color: var(--faint); font-size: 13px; white-space: nowrap; }
  .msg { margin-top: 12px; font-size: 13.5px; color: var(--dim); }
  .err { color: #B0393B; }
  #app { display: none; }
  .toolbar { justify-content: space-between; margin-top: 8px; }
  .foot { margin-top: 26px; font-size: 12.5px; color: var(--faint); }
  @media (max-width: 640px) { .hide-sm { display: none; } }
</style>
</head>
<body>
<div class="wrap">
  <h1>ZABEZ<span class="dot">.</span>com | Leads Console</h1>
  <p class="sub">Everyone who entered their email at the free-resource gate.</p>

  <div class="card" id="login">
    <div class="row">
      <input type="password" id="token" placeholder="Paste the export token" autocomplete="off">
      <button id="unlock">Unlock</button>
    </div>
    <p class="msg">The token lives on your Mac at ~/.zabez-leads-token. It is checked against the worker secret and kept only in this browser.</p>
    <p class="msg err" id="loginerr" style="display:none;">That token was rejected. Check it and try again.</p>
  </div>

  <div id="app">
    <div class="stats">
      <div class="stat"><b id="s-total">0</b><span>Total leads</span></div>
      <div class="stat"><b id="s-week">0</b><span>New in the last 7 days</span></div>
      <div class="stat"><b id="s-today">0</b><span>New today</span></div>
    </div>

    <div class="card">
      <div class="row toolbar">
        <div class="row">
          <input type="search" id="q" placeholder="Search email or resource">
          <button class="ghost" id="refresh">Refresh</button>
        </div>
        <div class="row">
          <button class="ghost" id="copy">Copy all emails</button>
          <button class="ghost" id="csv">Download CSV</button>
          <button id="bulk" disabled>Email selected via Gmail</button>
          <button class="ghost" id="logout">Log out</button>
        </div>
      </div>
      <div style="overflow-x:auto;">
        <table>
          <thead>
            <tr>
              <th><input type="checkbox" id="checkall"></th>
              <th>Email</th>
              <th>Requested</th>
              <th class="hide-sm">First seen</th>
              <th class="hide-sm">Last seen</th>
              <th class="hide-sm">Hits</th>
              <th>Send</th>
            </tr>
          </thead>
          <tbody id="rows"></tbody>
        </table>
      </div>
      <p class="msg" id="empty" style="display:none;">No leads captured yet. They will appear here the moment someone enters an email at the gate.</p>
    </div>

    <p class="foot">Sending opens a pre-filled Gmail compose from your own account, so replies land straight in your inbox. Bulk send puts everyone in BCC.</p>
  </div>
</div>

<script>
(function () {
  "use strict";
  var API = "/api/leads";
  var SITE = "https://zabez.com/";
  var RESOURCES = {
    "free/grc-resume-template.docx": { name: "GRC Resume Template", url: "https://zabez.com/free/grc-resume-template.docx" },
    "free/starter-policy-pack.docx": { name: "Starter Policy Pack", url: "https://zabez.com/free/starter-policy-pack.docx" },
    "free/what-is-grc.html": { name: "What Is GRC? guide", url: "https://zabez.com/free/what-is-grc.html" }
  };
  var leads = [];
  var el = function (id) { return document.getElementById(id); };

  function token() { return localStorage.getItem("zabez_admin_token") || ""; }

  function resourceInfo(file) {
    return RESOURCES[file] || { name: file || "resource", url: SITE + (file || "") };
  }

  function emailBody(lead) {
    var files = (lead && lead.files && lead.files.length) ? lead.files : Object.keys(RESOURCES);
    var lines = files.map(function (f) { var r = resourceInfo(f); return r.name + ": " + r.url; });
    return "Hi,\\n\\nThanks for grabbing resources from ZABEZ.com. Here is what you asked for:\\n\\n"
      + lines.join("\\n")
      + "\\n\\nYou are also on the daily GRC news digest: https://zabez.com/news/"
      + "\\n\\nIf you have any questions about breaking into GRC, just reply to this email. I read everything."
      + "\\n\\nKok Jabez\\nZABEZ.com | hi@zabez.com";
  }

  function gmailLink(to, bcc, lead) {
    var u = "https://mail.google.com/mail/?view=cm&fs=1"
      + "&su=" + encodeURIComponent("Your GRC downloads from ZABEZ.com")
      + "&body=" + encodeURIComponent(emailBody(lead));
    if (to) u += "&to=" + encodeURIComponent(to);
    if (bcc) u += "&bcc=" + encodeURIComponent(bcc);
    return u;
  }

  function fmt(iso) {
    if (!iso) return "";
    return iso.slice(0, 10) + " " + iso.slice(11, 16);
  }

  function render() {
    var q = el("q").value.trim().toLowerCase();
    var shown = leads.filter(function (l) {
      if (!q) return true;
      var hay = l.email + " " + (l.files || []).map(function (f) { return resourceInfo(f).name; }).join(" ");
      return hay.toLowerCase().indexOf(q) !== -1;
    });
    var body = el("rows");
    body.innerHTML = "";
    shown.forEach(function (l) {
      var tr = document.createElement("tr");
      tr.innerHTML =
        '<td><input type="checkbox" class="pick"></td>' +
        '<td class="email"></td>' +
        '<td class="files"></td>' +
        '<td class="muted hide-sm"></td>' +
        '<td class="muted hide-sm"></td>' +
        '<td class="muted hide-sm"></td>' +
        '<td></td>';
      tr.querySelector(".pick").value = l.email;
      tr.querySelector(".email").textContent = l.email;
      var filesTd = tr.querySelector(".files");
      (l.files || []).forEach(function (f) {
        var c = document.createElement("span");
        c.className = "chip";
        c.textContent = resourceInfo(f).name;
        filesTd.appendChild(c);
      });
      var tds = tr.querySelectorAll("td");
      tds[3].textContent = fmt(l.first_seen);
      tds[4].textContent = fmt(l.last_seen);
      tds[5].textContent = l.count || 1;
      var a = document.createElement("a");
      a.className = "btn";
      a.style.padding = "6px 14px";
      a.style.fontSize = "13px";
      a.target = "_blank";
      a.rel = "noopener";
      a.href = gmailLink(l.email, "", l);
      a.textContent = "Gmail";
      tds[6].appendChild(a);
      body.appendChild(tr);
    });
    el("empty").style.display = shown.length ? "none" : "block";
    wireChecks();
  }

  function wireChecks() {
    var picks = Array.prototype.slice.call(document.querySelectorAll(".pick"));
    function update() {
      var n = picks.filter(function (p) { return p.checked; }).length;
      el("bulk").disabled = n === 0;
      el("bulk").textContent = n ? "Email " + n + " selected via Gmail" : "Email selected via Gmail";
    }
    picks.forEach(function (p) { p.addEventListener("change", update); });
    el("checkall").onchange = function () {
      picks.forEach(function (p) { p.checked = el("checkall").checked; });
      update();
    };
    update();
  }

  function stats() {
    var now = Date.now();
    var day = 24 * 3600 * 1000;
    var todayStr = new Date().toISOString().slice(0, 10);
    el("s-total").textContent = leads.length;
    el("s-week").textContent = leads.filter(function (l) { return now - Date.parse(l.first_seen || 0) < 7 * day; }).length;
    el("s-today").textContent = leads.filter(function (l) { return (l.first_seen || "").slice(0, 10) === todayStr; }).length;
  }

  function load() {
    return fetch(API, { headers: { "Authorization": "Bearer " + token() } })
      .then(function (r) {
        if (r.status === 401) throw new Error("unauthorized");
        if (!r.ok) throw new Error("failed");
        return r.json();
      })
      .then(function (data) {
        leads = (data.leads || []).sort(function (a, b) {
          return (b.last_seen || "").localeCompare(a.last_seen || "");
        });
        el("login").style.display = "none";
        el("app").style.display = "block";
        stats();
        render();
      });
  }

  el("unlock").onclick = function () {
    localStorage.setItem("zabez_admin_token", el("token").value.trim());
    el("loginerr").style.display = "none";
    load().catch(function () {
      localStorage.removeItem("zabez_admin_token");
      el("loginerr").style.display = "block";
    });
  };
  el("token").addEventListener("keydown", function (e) { if (e.key === "Enter") el("unlock").click(); });

  el("refresh").onclick = function () { load().catch(function () {}); };
  el("q").addEventListener("input", render);
  el("logout").onclick = function () {
    localStorage.removeItem("zabez_admin_token");
    location.reload();
  };

  el("copy").onclick = function () {
    var all = leads.map(function (l) { return l.email; }).join(", ");
    navigator.clipboard.writeText(all).then(function () {
      el("copy").textContent = "Copied " + leads.length;
      setTimeout(function () { el("copy").textContent = "Copy all emails"; }, 1600);
    });
  };

  el("csv").onclick = function () {
    var head = "email,resources,first_seen,last_seen,count";
    var rows = leads.map(function (l) {
      var files = (l.files || []).map(function (f) { return resourceInfo(f).name; }).join("; ");
      return '"' + l.email + '","' + files.replace(/"/g, '""') + '","' + (l.first_seen || "") + '","' + (l.last_seen || "") + '",' + (l.count || 1);
    });
    var blob = new Blob([[head].concat(rows).join("\\n")], { type: "text/csv" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "zabez-leads-" + new Date().toISOString().slice(0, 10) + ".csv";
    a.click();
    URL.revokeObjectURL(a.href);
  };

  el("bulk").onclick = function () {
    var picked = Array.prototype.slice.call(document.querySelectorAll(".pick"))
      .filter(function (p) { return p.checked; })
      .map(function (p) { return p.value; });
    if (!picked.length) return;
    window.open(gmailLink("", picked.join(","), null), "_blank", "noopener");
  };

  if (token()) load().catch(function () { localStorage.removeItem("zabez_admin_token"); });
})();
</script>
</body>
</html>`;
