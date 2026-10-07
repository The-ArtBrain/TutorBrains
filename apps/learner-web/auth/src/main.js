import { createAuthClient } from "./client.js";

const config = window.BRAINOS_FIREBASE_CONFIG;
const nativeHostAvailable = window.BrainosNativeAuth?.version === 1;
if (!config?.enabled || (!nativeHostAvailable && location.origin !== config.courseOrigin)) {
  console.error("BrainOS authentication configuration is missing or does not match this course origin.");
} else {
  const client = createAuthClient(config);
  window.BrainosAuth = Object.freeze({
    getAuthView: () => client.getAuthView(),
    onAuthViewChange: (listener) => client.onAuthViewChange(listener),
  });

  const status = document.querySelector("[data-auth-status]");
  const nameForm = document.querySelector("[data-auth-name-form]");
  const editNameButton = document.querySelector("[data-auth-edit-name]");
  const nameInput = document.querySelector("#learner-name");
  const phoneForm = document.querySelector("[data-auth-phone-form]");
  const codeForm = document.querySelector("[data-auth-code-form]");
  const codeInput = document.querySelector("#phone-code");
  const signInLink = document.querySelector("[data-auth-sign-in]");
  const signOutItem = document.querySelector("[data-auth-sign-out]");
  const editProfileLink = document.querySelector("[data-auth-edit-profile]");
  const avatar = document.querySelector("[data-auth-avatar]");
  const displayName = document.querySelector("[data-auth-display-name]");
  const initials = document.querySelector("[data-auth-initials]");
  let completePhoneSignIn;

  function message(key) {
    return document.querySelector("main")?.dataset[key] || "";
  }

  function showError(error) {
    if (!status) return;
    const messages = {
      "auth/popup-closed-by-user": message("authCancelled"),
      "auth/popup-blocked": message("authPopupBlocked"),
      "auth/account-exists-with-different-credential": message("authExistingAccount"),
      "auth/credential-already-in-use": message("authCredentialInUse"),
      "auth/phone-number-already-exists": message("authCredentialInUse"),
      "auth/email-already-in-use": message("authCredentialInUse"),
      "auth/invalid-phone-number": message("authInvalidPhone"),
      "auth/invalid-verification-code": message("authInvalidCode"),
      "auth/too-many-requests": message("authTryLater"),
      "auth/operation-not-allowed": message("authProviderDisabled"),
      "auth/network-request-failed": message("authNetworkError"),
    };
    status.textContent = messages[error?.code] || message("authGenericError");
  }

  function render(view) {
    for (const button of document.querySelectorAll("[data-auth-provider]")) {
      button.disabled = !(config.enabledProviders || []).includes(button.dataset.authProvider);
      button.dataset.authLink = String(view.isAuthenticated);
    }
    const phoneEnabled = Boolean(config.phoneEnabled);
    const phoneNumber = phoneForm?.querySelector("input[type='tel']");
    const phoneButton = phoneForm?.querySelector("button[type='submit']");
    if (phoneNumber) phoneNumber.disabled = !phoneEnabled;
    if (phoneButton) phoneButton.disabled = !phoneEnabled;

    if (signInLink) signInLink.hidden = view.isAuthenticated;
    if (signOutItem) signOutItem.hidden = !view.isAuthenticated;
    if (editProfileLink) editProfileLink.hidden = !view.isAuthenticated;
    if (displayName) {
      displayName.textContent = view.displayName || "";
      displayName.hidden = !view.displayName;
    }
    if (avatar && view.avatarUrl) {
      avatar.src = view.avatarUrl;
      avatar.alt = "";
      avatar.hidden = false;
      avatar.onerror = () => {
        avatar.onerror = null;
        avatar.src = "assets/icons/user.svg";
        if (initials && view.initials) {
          initials.textContent = view.initials;
          initials.hidden = false;
          avatar.hidden = true;
        }
      };
      if (initials) initials.hidden = true;
    } else if (avatar) {
      avatar.src = "assets/icons/user.svg";
      avatar.hidden = false;
      if (initials) {
        initials.textContent = view.initials || "";
        initials.hidden = !view.initials;
        avatar.hidden = Boolean(view.initials);
      }
    }

    if (view.isAuthenticated && nameInput && nameForm && !view.displayName) {
      nameInput.value = view.displayName || "";
      nameForm.hidden = false;
      nameInput.focus({ preventScroll: true });
    }
    if (editNameButton) editNameButton.hidden = !view.isAuthenticated;
  }

  client.onAuthViewChange(render);

  editNameButton?.addEventListener("click", () => {
    client.getAuthView().then((view) => {
      nameInput.value = view.displayName || "";
      nameForm.hidden = false;
      nameInput.focus();
    });
  });
  editProfileLink?.addEventListener("click", (event) => {
    if (!nameForm || !nameInput) return;
    event.preventDefault();
    client.getAuthView().then((view) => {
      nameInput.value = view.displayName || "";
      nameForm.hidden = false;
      nameInput.focus();
    });
  });

  if (location.hash === "#edit-name" && nameForm && nameInput) {
    client.getAuthView().then((view) => {
      if (view.isAuthenticated) {
        nameInput.value = view.displayName || "";
        nameForm.hidden = false;
        nameInput.focus();
      }
    });
  }

  for (const button of document.querySelectorAll("[data-auth-provider]")) {
    button.addEventListener("click", async () => {
      if (status) status.textContent = "";
      try {
        const view = button.dataset.authLink === "true"
          ? await client.linkProvider(button.dataset.authProvider)
          : await client.signInWithProvider(button.dataset.authProvider);
        render(view);
      } catch (error) {
        showError(error);
      }
    });
  }

  phoneForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (status) status.textContent = "";
    const phone = phoneForm.querySelector("input[type='tel']").value.trim();
    try {
      completePhoneSignIn = await client.sendPhoneCode(phone, document.querySelector("[data-auth-recaptcha]"));
      codeForm.hidden = false;
      codeInput.focus();
      if (status) status.textContent = message("authCodeSent");
    } catch (error) {
      showError(error);
    }
  });

  codeForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!completePhoneSignIn) return;
    try {
      const view = await completePhoneSignIn(codeInput.value.trim());
      render(view);
      codeForm.hidden = true;
      if (status) status.textContent = message("authSignedIn");
    } catch (error) {
      showError(error);
    }
  });

  nameForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const view = await client.saveDisplayName(nameInput.value);
      render(view);
      nameForm.hidden = true;
      if (status) status.textContent = message("authNameSaved");
    } catch (error) {
      showError(error);
    }
  });

  signOutItem?.querySelector("button")?.addEventListener("click", async () => {
    try {
      await client.signOut();
      if (status) status.textContent = message("authSignedOut");
    } catch (error) {
      showError(error);
    }
  });
}
