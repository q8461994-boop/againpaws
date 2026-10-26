/* ------------------------------------------------------------------
   Again Paws — store settings
   Edit this file only. Everything else reads from here.
   ------------------------------------------------------------------ */
window.AP_STORE = {
  currency: "USD",
  symbol: "$",

  /* PayPal LIVE client ID — created in the merchant account.
     Where it came from: developer.paypal.com → Apps & Credentials
     → Live tab → the app created for this store → Client ID.
     If it is ever cleared, the cart hides PayPal and falls back to
     "order by email / WhatsApp" instead of breaking. */
  paypalClientId: "BAAImuoPzVJh29pTqlKWWQBDtWK_C9muWbxt6NT8fAYsM6vEfgu50xBrzxu-mkFAlmYPMqyv-1AIjQlSu0",

  /* Shipping charged at checkout, in dollars per order. */
  shipping: {
    flat: 9,        // e.g. 9 → $9.00 flat worldwide tracked shipping
    freeOver: 99    // e.g. 99 → free once the bag reaches $99.00
  },

  supportEmail: "q8461994@gmail.com",
  whatsapp: "8613064191721",
  storeName: "Again Paws"
};
