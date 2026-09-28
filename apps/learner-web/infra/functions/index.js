const COOKIE_NAME = "tb_instruction_language";
const DEFAULT_LANGUAGE = "en";
const SUPPORTED_LANGUAGES = new Set(["en", "hi"]);

function cookieLanguage(cookieHeader) {
  for (const cookie of (cookieHeader || "").split(";")) {
    const separator = cookie.indexOf("=");
    if (separator === -1 || cookie.slice(0, separator).trim() !== COOKIE_NAME) {
      continue;
    }

    try {
      const value = decodeURIComponent(cookie.slice(separator + 1).trim()).toLowerCase();
      return SUPPORTED_LANGUAGES.has(value) ? value : null;
    } catch {
      return null;
    }
  }
  return null;
}

function preferredLanguage(acceptLanguage) {
  const candidates = (acceptLanguage || "")
    .split(",")
    .map((entry, order) => {
      const [range, ...parameters] = entry.trim().toLowerCase().split(";");
      const language = range.split("-")[0];
      const qualityParameter = parameters.find((parameter) => parameter.trim().startsWith("q="));
      const quality = qualityParameter ? Number.parseFloat(qualityParameter.trim().slice(2)) : 1;
      return { language, order, quality: Number.isFinite(quality) ? quality : 0 };
    })
    .filter(({ language, quality }) => SUPPORTED_LANGUAGES.has(language) && quality > 0)
    .sort((left, right) => right.quality - left.quality || left.order - right.order);

  return candidates[0]?.language || DEFAULT_LANGUAGE;
}

export function selectLanguage(headers) {
  return cookieLanguage(headers.get("Cookie")) || preferredLanguage(headers.get("Accept-Language"));
}

export function onRequest({ request }) {
  if (request.method !== "GET" && request.method !== "HEAD") {
    return new Response("Method Not Allowed", {
      status: 405,
      headers: { Allow: "GET, HEAD" },
    });
  }

  const language = selectLanguage(request.headers);
  return new Response(null, {
    status: 307,
    headers: {
      "Cache-Control": "private, no-store",
      Location: `/${language}/index.html`,
      "Permissions-Policy": "camera=(), geolocation=(), microphone=()",
      "Referrer-Policy": "strict-origin-when-cross-origin",
      Vary: "Cookie, Accept-Language",
      "X-Content-Type-Options": "nosniff",
      "X-Frame-Options": "DENY",
    },
  });
}
