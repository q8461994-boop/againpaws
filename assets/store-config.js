/* ------------------------------------------------------------------
   Again Paws — store settings
   Edit this file only. Everything else reads from here.
   ------------------------------------------------------------------ */
window.AP_STORE = {
  currency: "USD",
  symbol: "$",

  /* PayPal client ID.
     Get it from https://developer.paypal.com/dashboard/applications
     → Apps & Credentials → Live → Client ID → copy.
     Paste it between the quotes below. Leave empty to hide PayPal
     buttons and fall back to "order by email / WhatsApp". */
  paypalClientId: "",

  /* Shipping charged at checkout, in dollars per order. */
  shipping: {
    flat: 9,        // e.g. 9 → $9.00 flat worldwide tracked shipping
    freeOver: 99    // e.g. 99 → free once the bag reaches $99.00
  },

  supportEmail: "q8461994@gmail.com",
  whatsapp: "8613064191721",
  storeName: "Again Paws"
};
