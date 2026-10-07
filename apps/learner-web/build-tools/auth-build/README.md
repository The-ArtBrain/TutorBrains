# Shared Firebase browser library

This folder contains only the pinned npm dependencies and build machinery for the shared authentication library. The JavaScript source and Firebase web configuration example remain in [`../../auth/`](../../auth/).

From the repository root, install the pinned dependencies and build the browser bundle:

```sh
npm ci --prefix apps/learner-web/build-tools/auth-build
npm run clean --prefix apps/learner-web/build-tools/auth-build
npm run build --prefix apps/learner-web/build-tools/auth-build
```

`npm run clean` removes only the generated bundle (`apps/learner-web/dist/auth.js`). The npm build reads `../../auth/src/main.js` and writes a fresh bundle directly to `apps/learner-web/dist/auth.js`, not to a local `dist/` beside the npm files. This is a shared intermediate artifact, not a deployable course root. To include it in a course build, provide that course's local Firebase configuration from `apps/learner-web/auth/` to `apps/learner-web/build-tools/build.py`. The static build copies the bundle into the generated site at `apps/learner-web/dist/<distribution-root>/<language>/assets/js/firebase-auth.js` and inserts its script tag into generated HTML. Without `--firebase-config`, authentication remains disabled and the npm bundle is not copied into the published course site.

Use [`../README.md`](../README.md) for the complete build workflow and [`../../../../doc/design/FIREBASE_AUTH_DESIGN.md`](../../../../doc/design/FIREBASE_AUTH_DESIGN.md) for Firebase setup, provider configuration, and per-course config instructions. Never commit course-local config files or provider secrets.
