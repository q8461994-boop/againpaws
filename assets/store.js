/* ------------------------------------------------------------------
   Again Paws — bag + checkout (no backend)
   - Cart lives in localStorage
   - PayPal orders are created + captured in the browser (JS SDK)
   - If no client ID is configured, checkout falls back to email/WhatsApp
   ------------------------------------------------------------------ */
(function () {
  "use strict";

  var CFG = window.AP_STORE || {};
  var KEY = "ap_cart_v1";
  var LAST = "ap_last_order_v1";
  var CUR = CFG.currency || "USD";
  var SYM = CFG.symbol || "$";

  /* ---------- helpers ---------- */
  function money(c) { return SYM + (Number(c) / 100).toFixed(2); }
  function d2c(v) { return Math.round((Number(v) || 0) * 100); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (m) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m];
    });
  }
  function track(name, payload) {
    if (typeof window.gtag === "function") {
      try { window.gtag("event", name, payload || {}); } catch (e) {}
    }
  }

  /* ---------- state ---------- */
  var items = load();

  function load() {
    try {
      var raw = JSON.parse(localStorage.getItem(KEY) || "[]");
      if (!Array.isArray(raw)) return [];
      return raw.map(function (i) {
        if (!i || !i.id || !(i.qty > 0)) return null;
        i.qty = Math.min(99, parseInt(i.qty, 10) || 1);
        i.price = Math.round(Number(i.price) || 0);
        return i;
      }).filter(Boolean);
    } catch (e) { return []; }
  }

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) {}
    paint();
  }

  function subtotal() {
    return items.reduce(function (s, i) { return s + i.price * i.qty; }, 0);
  }
  function count() {
    return items.reduce(function (s, i) { return s + i.qty; }, 0);
  }
  function shipCfg() {
    var s = CFG.shipping || {};
    return { flat: d2c(s.flat), freeOver: d2c(s.freeOver) };
  }
  function shipping() {
    var s = shipCfg(), sub = subtotal();
    if (!items.length) return 0;
    if (!s.flat) return 0;
    if (s.freeOver && sub >= s.freeOver) return 0;
    return s.flat;
  }
  function total() { return subtotal() + shipping(); }

  function add(item) {
    var found = null;
    for (var i = 0; i < items.length; i++) if (items[i].id === item.id) found = items[i];
    if (found) found.qty = Math.min(99, found.qty + item.qty);
    else items.push(item);
    save();
    track("add_to_cart", { currency: CUR, value: (item.price * item.qty) / 100, items: item.name });
  }
  function setQty(id, qty) {
    for (var i = 0; i < items.length; i++) {
      if (items[i].id === id) {
        items[i].qty = Math.max(0, Math.min(99, qty));
        if (!items[i].qty) items.splice(i, 1);
        break;
      }
    }
    save();
  }
  function remove(id) {
    items = items.filter(function (i) { return i.id !== id; });
    save();
  }

  /* ---------- markup ---------- */
  function shipNote() {
    var s = shipCfg();
    if (!s.flat) return "Worldwide tracked shipping calculated after ordering.";
    var txt = money(s.flat) + " flat-rate tracked shipping";
    if (s.freeOver) txt += " · free over " + money(s.freeOver);
    return txt + " · duties and taxes, if any, are collected on delivery.";
  }

  function lineHTML(i, compact) {
    return '' +
      '<div class="cart-line' + (compact ? ' is-compact' : '') + '">' +
        '<div class="cart-thumb">' + (i.img ? '<img src="' + esc(i.img) + '" alt="' + esc(i.name) + '"/>' : '') + '</div>' +
        '<div class="cart-line-main">' +
          '<p class="cart-line-name">' + esc(i.name) + '</p>' +
          (i.variant ? '<p class="cart-line-variant">' + esc(i.variant) + '</p>' : '') +
          '<div class="cart-line-actions">' +
            '<div class="qty qty-sm">' +
              '<button type="button" data-cart-dec="' + esc(i.id) + '" aria-label="Decrease quantity">−</button>' +
              '<span>' + i.qty + '</span>' +
              '<button type="button" data-cart-inc="' + esc(i.id) + '" aria-label="Increase quantity">+</button>' +
            '</div>' +
            '<button type="button" class="link-quiet" data-cart-rm="' + esc(i.id) + '">Remove</button>' +
          '</div>' +
        '</div>' +
        '<div class="cart-line-price">' + money(i.price * i.qty) + '</div>' +
      '</div>';
  }

  function emptyHTML(drawer) {
    return '' +
      '<div class="cart-empty">' +
        '<p class="eyebrow">Nothing here yet</p>' +
        '<p class="lead">' + (drawer ? "Your bag is empty." : "Your bag is empty — the Memorial Collection is a good place to start.") + '</p>' +
        '<div class="btn-row"><a class="btn btn-primary btn-sm" href="/products/#memorial">Browse the collection</a></div>' +
      '</div>';
  }

  /* ---------- paint ---------- */
  function paint() {
    var n = count();
    Array.prototype.forEach.call(document.querySelectorAll("[data-cart-count]"), function (el) {
      el.textContent = n;
      el.hidden = n === 0;
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-ship-note]"), function (el) {
      el.textContent = shipNote();
    });
    paintDrawer();
    paintCartPage();
  }

  function paintDrawer() {
    var list = document.getElementById("cartDrawerList");
    var foot = document.getElementById("cartDrawerFoot");
    if (!list || !foot) return;
    if (!items.length) {
      list.innerHTML = emptyHTML(true);
      foot.innerHTML = "";
      foot.hidden = true;
      return;
    }
    foot.hidden = false;
    list.innerHTML = items.map(function (i) { return lineHTML(i, true); }).join("");
    foot.innerHTML =
      '<div class="sum-row"><span>Subtotal</span><b>' + money(subtotal()) + '</b></div>' +
      '<p class="cart-mini">' + esc(shipNote()) + '</p>' +
      '<a class="btn btn-primary cart-wide" href="/cart/">Checkout</a>' +
      '<button type="button" class="link-quiet cart-wide" data-cart-close>Keep shopping</button>';
  }

  function paintCartPage() {
    var app = document.getElementById("cartApp");
    if (!app) return;
    var side = document.getElementById("cartSide");
    if (!items.length) {
      app.innerHTML = emptyHTML(false);
      if (side) {
        side.innerHTML = "";
        side.hidden = true;
        delete side.dataset.built;   // rebuild the summary when something is added again
        paypalMounted = false;
      }
      return;
    }
    app.innerHTML = '<div class="cart-lines">' + items.map(function (i) { return lineHTML(i, false); }).join("") + '</div>';
    if (side) {
      side.hidden = false;
      if (!side.dataset.built) {
        side.innerHTML =
          '<div class="card cart-summary">' +
            '<h3>Order summary</h3>' +
            '<dl class="sum-list">' +
              '<div class="sum-row"><dt>Subtotal</dt><dd id="sumSub">—</dd></div>' +
              '<div class="sum-row"><dt>Shipping</dt><dd id="sumShip">—</dd></div>' +
              '<div class="sum-row is-total"><dt>Total</dt><dd id="sumTotal">—</dd></div>' +
            '</dl>' +
            '<p class="cart-mini" id="sumShipNote"></p>' +
            '<div id="paypalArea" class="paypal-area"></div>' +
            '<div class="pay-notes">' +
              '<p>Secure checkout by PayPal. Pay with a PayPal balance, a linked card, or as a guest with any debit or credit card — no PayPal account needed.</p>' +
              '<p>Orders ship from our workshop within 3–10 working days. You will get a tracking number by email.</p>' +
            '</div>' +
          '</div>' +
          '<div class="cart-help">' +
            '<h3>Need something custom?</h3>' +
            '<p>Felted portraits and engraving text are quoted by hand. <a href="/contact/">Send us a photo</a> and we will reply within 24 hours.</p>' +
          '</div>';
        side.dataset.built = "1";
        mountPayPal();
      }
      var sub = document.getElementById("sumSub");
      if (sub) {
        document.getElementById("sumSub").textContent = money(subtotal());
        document.getElementById("sumShip").textContent = shipping() ? money(shipping()) : "Free";
        document.getElementById("sumTotal").textContent = money(total());
        document.getElementById("sumShipNote").textContent = shipNote();
      }
    }
  }

  /* ---------- PayPal ---------- */
  function payPalReady(cb) {
    if (!CFG.paypalClientId) { cb(false); return; }
    if (window.paypal && window.paypal.Buttons) { cb(true); return; }
    var s = document.createElement("script");
    s.src = "https://www.paypal.com/sdk/js?client-id=" + encodeURIComponent(CFG.paypalClientId) +
            "&currency=" + encodeURIComponent(CUR) + "&intent=capture&components=buttons";
    s.async = true;
    s.onload = function () { cb(!!(window.paypal && window.paypal.Buttons)); };
    s.onerror = function () { cb(false); };
    document.head.appendChild(s);
  }

  function orderPayload() {
    var sub = subtotal(), ship = shipping(), tot = total();
    var its = items.map(function (i) {
      return {
        name: (i.name + (i.variant ? " — " + i.variant : "")).slice(0, 127),
        quantity: String(i.qty),
        unit_amount: { currency_code: CUR, value: (i.price / 100).toFixed(2) },
        category: "PHYSICAL_GOODS",
        sku: String(i.id).slice(0, 127)
      };
    });
    return {
      purchase_units: [{
        description: "Again Paws order",
        items: its,
        amount: {
          currency_code: CUR,
          value: (tot / 100).toFixed(2),
          breakdown: {
            item_total: { currency_code: CUR, value: (sub / 100).toFixed(2) },
            shipping: { currency_code: CUR, value: (ship / 100).toFixed(2) }
          }
        }
      }],
      application_context: {
        brand_name: CFG.storeName || "Again Paws",
        shipping_preference: "GET_FROM_FILE",
        user_action: "PAY_NOW"
      }
    };
  }

  function fallbackHTML(reason) {
    var lines = items.map(function (i) {
      return i.qty + " × " + i.name + (i.variant ? " (" + i.variant + ")" : "") + " — " + money(i.price * i.qty);
    });
    var body = "Hi Again Paws,\n\nI would like to order:\n\n" + lines.join("\n") +
      "\n\nSubtotal: " + money(subtotal()) +
      "\nShipping: " + (shipping() ? money(shipping()) : "Free") +
      "\nTotal: " + money(total()) +
      "\n\nPlease send me a PayPal invoice or a payment link.\n\nName:\nShipping address:\nNotes:\n";
    var mail = "mailto:" + (CFG.supportEmail || "q8461994@gmail.com") +
      "?subject=" + encodeURIComponent("Order — " + count() + " item" + (count() > 1 ? "s" : "") + " — " + money(total())) +
      "&body=" + encodeURIComponent(body);
    var wa = "https://wa.me/" + (CFG.whatsapp || "") + "?text=" + encodeURIComponent(body);
    return '' +
      (reason ? '<p class="pay-fallback-note">' + esc(reason) + '</p>' : '') +
      '<p class="pay-fallback">Prefer an invoice? Send us the bag and we will email a PayPal payment link.</p>' +
      '<a class="btn btn-stone cart-wide" href="' + esc(mail) + '">Email this order</a>' +
      '<a class="btn btn-outline-stone cart-wide" href="' + esc(wa) + '" target="_blank" rel="noopener">Send on WhatsApp</a>';
  }

  var paypalMounted = false;
  function mountPayPal() {
    var area = document.getElementById("paypalArea");
    if (!area || paypalMounted) return;
    paypalMounted = true;

    if (!CFG.paypalClientId) {
      area.innerHTML = fallbackHTML("");
      return;
    }
    area.innerHTML = '<p class="pay-loading">Loading secure checkout…</p>';
    payPalReady(function (ok) {
      if (!ok) {
        area.innerHTML = fallbackHTML("PayPal did not load — you can still order by email.");
        return;
      }
      area.innerHTML = "";
      var holder = document.createElement("div");
      holder.id = "paypalButtons";
      area.appendChild(holder);
      try {
        window.paypal.Buttons({
          style: { layout: "vertical", shape: "pill", color: "gold", label: "paypal", height: 48, tagline: false },
          createOrder: function (data, actions) { return actions.order.create(orderPayload()); },
          onApprove: function (data, actions) {
            return actions.order.capture().then(function (details) {
              var id = (details && details.id) || data.orderID || "";
              var paid = details && details.purchase_units && details.purchase_units[0] &&
                         details.purchase_units[0].amount && details.purchase_units[0].amount.value;
              var snapshot = items.slice();
              try {
                localStorage.setItem(LAST, JSON.stringify({
                  id: id, total: paid || (total() / 100).toFixed(2),
                  currency: CUR, items: snapshot, at: new Date().toISOString()
                }));
              } catch (e) {}
              track("purchase", { transaction_id: id, value: Number(paid) || total() / 100, currency: CUR });
              items = [];
              try { localStorage.removeItem(KEY); } catch (e) {}
              window.location.href = "/thank-you/?order=" + encodeURIComponent(id) +
                (paid ? "&total=" + encodeURIComponent(paid) : "");
            });
          },
          onError: function (err) {
            var p = document.getElementById("paypalMsg");
            if (!p) {
              p = document.createElement("p");
              p.id = "paypalMsg";
              p.className = "pay-error";
              area.appendChild(p);
            }
            p.textContent = "That payment did not go through. Nothing was charged — please try again or email us.";
          },
          onCancel: function () { /* buyer closed the window */ }
        }).render(holder);
      } catch (e) {
        area.innerHTML = fallbackHTML("PayPal could not start on this device.");
      }
    });
  }

  /* ---------- add to bag from product pages ---------- */
  function qtyInput() {
    var el = document.getElementById("qtyInput");
    var n = el ? parseInt(el.value, 10) : 1;
    return Math.max(1, Math.min(99, n || 1));
  }

  document.addEventListener("click", function (e) {
    var t = e.target;

    var addBtn = t.closest("[data-add]");
    if (addBtn) {
      e.preventDefault();
      var d = addBtn.dataset;
      add({
        id: d.id,
        slug: d.slug || "",
        name: d.name,
        variant: d.variant || "",
        price: parseInt(d.price, 10) || 0,
        img: d.img || "",
        qty: qtyInput()
      });
      openDrawer();
      return;
    }

    var dec = t.closest("[data-cart-dec]");
    if (dec) {
      var id = dec.getAttribute("data-cart-dec");
      var cur = (items.filter(function (i) { return i.id === id; })[0] || {}).qty || 1;
      setQty(id, cur - 1);
      return;
    }
    var inc = t.closest("[data-cart-inc]");
    if (inc) {
      var id2 = inc.getAttribute("data-cart-inc");
      var cur2 = (items.filter(function (i) { return i.id === id2; })[0] || {}).qty || 0;
      setQty(id2, cur2 + 1);
      return;
    }
    var rm = t.closest("[data-cart-rm]");
    if (rm) {
      remove(rm.getAttribute("data-cart-rm"));
      return;
    }
    if (t.closest("[data-cart-close]")) { closeDrawer(); return; }
  });

  /* qty steppers on product pages */
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-qty]");
    if (!b) return;
    var input = document.getElementById("qtyInput");
    if (!input) return;
    var step = parseInt(b.getAttribute("data-qty"), 10) || 1;
    input.value = Math.max(1, Math.min(99, (parseInt(input.value, 10) || 1) + step));
  });

  /* ---------- drawer ---------- */
  function openDrawer() {
    var d = document.getElementById("cartDrawer");
    if (!d) return;
    d.hidden = false;
    d.setAttribute("aria-hidden", "false");
    document.documentElement.classList.add("is-locked");
    requestAnimationFrame(function () { d.classList.add("is-open"); });
    var c = d.querySelector(".drawer-close");
    if (c) c.focus();
  }
  function closeDrawer() {
    var d = document.getElementById("cartDrawer");
    if (!d) return;
    d.classList.remove("is-open");
    d.setAttribute("aria-hidden", "true");
    document.documentElement.classList.remove("is-locked");
    setTimeout(function () { d.hidden = true; }, 220);
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeDrawer();
  });

  /* ---------- boot ---------- */
  paint();
  // keep multiple tabs in sync
  window.addEventListener("storage", function (e) {
    if (e.key === KEY) { items = load(); paint(); }
  });

  window.APCart = {
    items: function () { return items.slice(); },
    add: add, setQty: setQty, remove: remove,
    subtotal: subtotal, shipping: shipping, total: total, money: money
  };
})();
