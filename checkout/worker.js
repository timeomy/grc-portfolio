/**
 * Zabez GRC course checkout — Cloudflare Worker
 *
 * Creates a Billplz payment bill for the GRC Analyst Program.
 * Deploy this as a Cloudflare Worker (free tier), set secrets, done.
 *
 * SETUP:
 *  1. wrangler secret put BILLPLZ_API_KEY        (your Billplz API key)
 *  2. wrangler secret put BILLPLZ_COLLECTION_ID  (your course collection ID)
 *  3. wrangler deploy
 *  4. Put the worker URL in checkout.js on the site
 *
 * Billplz API docs: https://www.billplz.com/api
 * Amount is in SEN (RM 1 = 100 sen). Price set below.
 */

const PRICE_SEN = 499 * 100; // RM 499
const DESCRIPTION = "GRC Analyst Program — lifetime access";
const CALLBACK_URL = "https://zabez.com/courses/thanks.html"; // server notification
const REDIRECT_URL = "https://zabez.com/courses/thanks.html";  // buyer lands here after paying
const REFERENCE_LABEL = "Order";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: corsHeaders(),
      });
    }

    // Email gate: capture a lead, store it in KV, reveal the download.
    // Accepts form-encoded or JSON. Requires the LEADS KV binding.
    if (request.method === "POST" && url.pathname === "/api/subscribe") {
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
    if (request.method === "GET" && url.pathname === "/api/leads") {
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

    if (request.method === "POST" && url.pathname === "/api/checkout") {
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

    return json({ error: "Not found" }, 404);
  },
};

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
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}
