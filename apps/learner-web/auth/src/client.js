import { initializeApp } from "firebase/app";
import {
  FacebookAuthProvider,
  GoogleAuthProvider,
  OAuthProvider,
  RecaptchaVerifier,
  TwitterAuthProvider,
  browserLocalPersistence,
  indexedDBLocalPersistence,
  initializeAuth,
  linkWithPhoneNumber,
  linkWithPopup,
  onAuthStateChanged,
  signInWithPhoneNumber,
  signInWithPopup,
  signOut,
  updateProfile,
} from "firebase/auth";

const factories = {
  google: () => new GoogleAuthProvider(),
  apple: () => new OAuthProvider("apple.com"),
  facebook: () => new FacebookAuthProvider(),
  microsoft: () => new OAuthProvider("microsoft.com"),
  x: () => new TwitterAuthProvider(),
  linkedin: () => new OAuthProvider("oidc.linkedin"),
};

function makeProvider(name) {
  if (!Object.prototype.hasOwnProperty.call(factories, name)) throw new Error("Unsupported sign-in provider");
  const provider = factories[name]();
  if (name === "microsoft" || name === "linkedin") provider.addScope("email");
  return provider;
}

function view(user) {
  if (!user) return Object.freeze({ isAuthenticated: false, userId: null, displayName: null, avatarUrl: null, initials: null, hasEmail: false });
  const displayName = user.displayName?.trim() || null;
  const initials = displayName?.split(/\s+/u).slice(0, 2).map((word) => word[0]).join("").toLocaleUpperCase() || null;
  const avatarUrl = user.photoURL?.startsWith("https://") ? user.photoURL : null;
  return Object.freeze({ isAuthenticated: true, userId: user.uid, displayName, avatarUrl, initials, hasEmail: Boolean(user.email && user.emailVerified) });
}

export function createAuthClient(config) {
  const nativeHost = window.BrainosNativeAuth;
  if (nativeHost?.version === 1) {
    let current = Object.freeze({ isAuthenticated: false, userId: null, displayName: null, avatarUrl: null, initials: null, hasEmail: false });
    const listeners = new Set();
    const safeView = (candidate) => {
      if (!candidate?.isAuthenticated || typeof candidate.userId !== "string") {
        return Object.freeze({ isAuthenticated: false, userId: null, displayName: null, avatarUrl: null, initials: null, hasEmail: false });
      }
      return Object.freeze({
        isAuthenticated: true,
        userId: candidate.userId,
        displayName: typeof candidate.displayName === "string" ? candidate.displayName : null,
        avatarUrl: typeof candidate.avatarUrl === "string" && candidate.avatarUrl.startsWith("https://") ? candidate.avatarUrl : null,
        initials: typeof candidate.initials === "string" ? candidate.initials : null,
        hasEmail: Boolean(candidate.hasEmail),
      });
    };
    nativeHost.onAuthViewChange((candidate) => {
      current = safeView(candidate);
      for (const listener of listeners) listener(current);
    });
    return {
      async getAuthView() { current = safeView(await nativeHost.getAuthView()); return current; },
      onAuthViewChange(listener) { listeners.add(listener); nativeHost.getAuthView().then((value) => listener(safeView(value))); return () => listeners.delete(listener); },
      async signInWithProvider(name) { return safeView(await nativeHost.signInWithProvider(name)); },
      async linkProvider(name) { return safeView(await nativeHost.linkProvider(name)); },
      async sendPhoneCode(phone) {
        await nativeHost.sendPhoneCode(phone);
        return async (code) => safeView(await nativeHost.confirmPhoneCode(code));
      },
      async saveDisplayName(name) { return safeView(await nativeHost.saveDisplayName(name)); },
      async signOut() { await nativeHost.signOut(); },
    };
  }

  const app = initializeApp(config.firebase);
  const auth = initializeAuth(app, { persistence: [indexedDBLocalPersistence, browserLocalPersistence] });
  auth.languageCode = document.documentElement.lang.slice(0, 2);
  let current = view(null);
  const listeners = new Set();
  const ready = new Promise((resolve) => {
    onAuthStateChanged(auth, (user) => {
      current = view(user);
      for (const listener of listeners) listener(current);
      resolve(current);
    });
  });

  return {
    async getAuthView() { await ready; return current; },
    onAuthViewChange(listener) { listeners.add(listener); listener(current); return () => listeners.delete(listener); },
    async signInWithProvider(name) {
      const result = await signInWithPopup(auth, makeProvider(name));
      return view(result.user);
    },
    async linkProvider(name) {
      await ready;
      if (!auth.currentUser) throw new Error("Sign in before linking another provider");
      const result = await linkWithPopup(auth.currentUser, makeProvider(name));
      return view(result.user);
    },
    async sendPhoneCode(phone, recaptchaElement) {
      const verifier = new RecaptchaVerifier(auth, recaptchaElement, { size: "normal" });
      try {
        const confirmation = auth.currentUser
          ? await linkWithPhoneNumber(auth.currentUser, phone, verifier)
          : await signInWithPhoneNumber(auth, phone, verifier);
        return async (code) => {
          const result = await confirmation.confirm(code);
          verifier.clear();
          return view(result.user);
        };
      } catch (error) {
        verifier.clear();
        throw error;
      }
    },
    async saveDisplayName(name) {
      await ready;
      const user = auth.currentUser;
      if (!user) throw new Error("Sign in before saving a name");
      const cleaned = name.trim().replace(/\s+/gu, " ");
      if (!cleaned || cleaned.length > 80) throw new Error("Name must be between 1 and 80 characters");
      await updateProfile(user, { displayName: cleaned });
      current = view(user);
      for (const listener of listeners) listener(current);
      return current;
    },
    async signOut() { await signOut(auth); },
  };
}
