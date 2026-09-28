(() => {
  "use strict";

  const match = window.location.pathname.match(/^\/(en|hi)(?:\/|$)/);
  if (!match) {
    return;
  }

  document.cookie = [
    `tb_instruction_language=${match[1]}`,
    "Path=/",
    "Max-Age=31536000",
    "Secure",
    "SameSite=Lax",
  ].join("; ");
})();
