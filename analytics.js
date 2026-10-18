(() => {
  const measurementId = "G-KKE2MPQSCL";
  window.dataLayer = window.dataLayer || [];
  function gtag(){ window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;
  gtag("js", new Date());
  gtag("config", measurementId, { send_page_view: false });

  function trackPageView() {
    gtag("event", "page_view", {
      page_location: window.location.href,
      page_path: window.location.pathname + window.location.search,
      page_title: document.title
    });
  }

  function trackRouteChange() {
    window.setTimeout(trackPageView, 0);
  }

  const originalPushState = history.pushState;
  history.pushState = function () {
    const result = originalPushState.apply(this, arguments);
    trackRouteChange();
    return result;
  };

  const originalReplaceState = history.replaceState;
  history.replaceState = function () {
    const result = originalReplaceState.apply(this, arguments);
    trackRouteChange();
    return result;
  };

  window.addEventListener("popstate", trackRouteChange);
  document.addEventListener("click", (event) => {
    const link = event.target.closest("a[href]");
    if (!link) return;

    const href = link.href || "";
    let contactMethod = "";
    if (/^https:\/\/wa\.me\//i.test(href)) contactMethod = "whatsapp";
    if (/^mailto:/i.test(href)) contactMethod = "email";
    if (!contactMethod) return;

    gtag("event", "generate_lead", {
      contact_method: contactMethod,
      link_url: href.split("?")[0]
    });
  });

  trackPageView();
})();
