# TutorBrains

A subject-neutral learning platform. Telugu Tutor is its first focused product.

## Learner web commands

Install the end-to-end test dependencies once from the repository root, then run the tests. Playwright uses Google Chrome Stable (`channel: "chrome"`):

```sh
npm ci --prefix tests/end-to-end/learner-web
npm --prefix tests/end-to-end/learner-web test
```

Debug one test with Playwright Inspector, replacing `TC-16` as needed:

```sh
npm --prefix tests/end-to-end/learner-web test -- --debug --grep "TC-16"
```

Watch the complete suite run in a visible browser:

```sh
npm --prefix tests/end-to-end/learner-web test -- --headed --workers=1
```

Run the Python build-tool unit tests with `uv` using the build tool's `pyproject.toml`:

```sh
uv run --project apps/learner-web/build-tools --group build python -m unittest discover -s apps/learner-web/build-tools/tests -v
```

Set up the build environment once, then generate the English and Hindi pages from the repository root:

```sh
python3 -m venv apps/learner-web/build-tools/.venv
apps/learner-web/build-tools/.venv/bin/python -m pip install --group apps/learner-web/build-tools/pyproject.toml:build
apps/learner-web/build-tools/.venv/bin/python apps/learner-web/build-tools/build.py
apps/learner-web/build-tools/.venv/bin/python apps/learner-web/build-tools/build.py --instruction-language hi
```

Alternatively, let `uv` provide the build environment without creating the project-local virtual environment manually:

```sh
uv run --project apps/learner-web/build-tools --group build python apps/learner-web/build-tools/build.py
uv run --project apps/learner-web/build-tools --group build python apps/learner-web/build-tools/build.py --instruction-language hi
```

The defaults are English instructions, the Telugu course, the `practical-telugu` content folder, and the `telugu` distribution root; output is published below `apps/learner-web/dist/telugu/en/` and `dist/telugu/hi/`. Open the generated `index.html` in either language directory. Application pages use top-level `content/<page>.<language>.yml` files. Generic chapter and lesson HTML sources are filled from the selected course's chapter and lesson folders, producing identity-specific filenames. See [`apps/learner-web/build-tools/README.md`](apps/learner-web/build-tools/README.md) for conventions, parameters, and unit tests. Browser tests build both languages automatically using this environment (or `LEARNER_WEB_PYTHON`).

Remove all generated learner-web output with `python3 apps/learner-web/build-tools/build.py clean`.

## Manual Docker build without the Cloudflare helper

Use these commands instead of `deploy-cloudflare-pages.sh` when you want to run the build and optional upload manually. Run the setup commands from the repository root on the host. The remaining commands are entered in the container's interactive Bash terminal.

Build the image and choose the persistent container name:

```sh
docker compose -f apps/learner-web/infra/compose.yaml build wrangler
export WRANGLER_CONTAINER="${CLOUDFLARE_WRANGLER_CONTAINER:-telugututorbrains}"
```

Create the persistent container once, if it does not already exist. Skip this command for an existing container. If it exists but is stopped, start it with `docker start "${WRANGLER_CONTAINER}"` instead.

```sh
docker compose -f apps/learner-web/infra/compose.yaml run --detach --no-deps --name "${WRANGLER_CONTAINER}" --entrypoint /bin/sh wrangler -c 'while :; do sleep 3600; done'
```

Open an interactive terminal in that running container:

```sh
docker exec -it "${WRANGLER_CONTAINER}" bash
```

Run the remaining commands below from that container terminal. Run the build-tool unit tests and browser tests:

```sh
/opt/brainos-build-venv/bin/python -m unittest discover -s /workspace/apps/learner-web/build-tools/tests -v

mkdir -p /workspace/tests/end-to-end/learner-web/node_modules/@playwright
ln -sfn /opt/brainos-e2e-review/node_modules/@playwright/test \
  /workspace/tests/end-to-end/learner-web/node_modules/@playwright/test
LEARNER_WEB_PYTHON=/opt/brainos-build-venv/bin/python \
PLAYWRIGHT_OUTPUT_DIR=/tmp/learner-web-test-results \
npm --prefix /opt/brainos-e2e-review test -- \
  --config /workspace/tests/end-to-end/learner-web/playwright.config.js
```

Clean generated course outputs, then clean and build the shared authentication bundle:

```sh
/opt/brainos-build-venv/bin/python /workspace/apps/learner-web/build-tools/build.py clean

BRAINOS_AUTH_ENTRY=/workspace/apps/learner-web/auth/src/main.js \
BRAINOS_AUTH_OUTFILE=/workspace/apps/learner-web/dist/auth.js \
  npm --prefix /opt/brainos-auth-build run clean

BRAINOS_AUTH_ENTRY=/workspace/apps/learner-web/auth/src/main.js \
BRAINOS_AUTH_OUTFILE=/workspace/apps/learner-web/dist/auth.js \
  npm --prefix /opt/brainos-auth-build run build
```

Build English and Hindi output. If Firebase authentication is configured, add `--firebase-config /workspace/<path-to-config.json>` to both Python build commands; the file must be under the mounted repository.

```sh
/opt/brainos-build-venv/bin/python /workspace/apps/learner-web/build-tools/build.py --distribution-root telugu

/opt/brainos-build-venv/bin/python \
  /workspace/apps/learner-web/build-tools/build.py \
  --instruction-language hi --distribution-root telugu
```

Stage the Cloudflare policies and verify the generated root:

```sh
for policy in _headers _redirects _routes.json; do
  if [ -f "/workspace/apps/learner-web/infra/policies/$policy" ]; then
    cp "/workspace/apps/learner-web/infra/policies/$policy" \
      "/workspace/apps/learner-web/dist/telugu/$policy"
  fi
done
test -s /workspace/apps/learner-web/dist/telugu/index.html
test -s /workspace/apps/learner-web/dist/telugu/en/index.html
test -s /workspace/apps/learner-web/dist/telugu/hi/index.html
test -s /workspace/apps/learner-web/dist/telugu/_headers
test -s /workspace/apps/learner-web/dist/telugu/_routes.json
```

The resulting artifact is available on the host at `apps/learner-web/dist/telugu/`. To upload it manually with Wrangler, ensure `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN` are available inside the container from your approved secret store, then run this from the container terminal:

```sh
: "${CLOUDFLARE_ACCOUNT_ID:?Load this from the approved secret store}"
: "${CLOUDFLARE_API_TOKEN:?Load this from the approved secret store}"
: "${CLOUDFLARE_BRANCH:?Choose a preview or production branch label}"

wrangler pages deploy /workspace/apps/learner-web/dist/telugu \
  --project-name "${CLOUDFLARE_PAGES_PROJECT:-telugututorbrains}" \
  --branch "${CLOUDFLARE_BRANCH}"
```

Manual upload bypasses the branch, clean-worktree, and confirmation safeguards in `deploy-cloudflare-pages.sh`.

## Product specifications

- [Student onboarding guide](doc/spec/student_onboarding_guide.md) — student actions before Chapter 01, mapped to the capability catalogue.
- [Common product specification](doc/spec/common_spec.md) — tutor behaviour inherited by every chapter.
- [Chapter 01 Tutor Product Requirements Document](doc/spec/CHAPTER_01_TUTOR_PRD.md) — the first guided greeting lesson.
- [Capability matrix](doc/spec/capability_matrix.md) — technology-neutral product capabilities and ability-based authorization.
- [Platform and logical presentation specification](doc/spec/platform_spec.md) — required platforms, local-intelligence boundaries, component inventory, and the card model.
- [Character units](doc/spec/characters_spec.md), [grammar units](doc/spec/grammar_spec.md), [vocabulary units](doc/spec/vocabulary_spec.md), and [sentence units](doc/spec/sentence_spec.md) — reusable learning-unit definitions.

## Technical designs

- [Architecture Decision Record log](doc/design/ARCHITECTURE_DECISION_LOG.md) — current fixed, accepted, proposed, and deferred architecture decisions.
- [Proposed project structure](doc/design/project_structure.md) — subject-neutral repository organization and build-time specialization boundaries.
- [App skeleton technical design](doc/design/APP_SKELETON_TECH_DESIGN.md) — shared semantic HTML and standard JavaScript architecture, platform-service contracts, and comparison of three potential schemes.
- [Progressive Web App platform design](doc/design/PWA_PLATFORM_DESIGN.md) — browser-installed candidate and its required-platform proof burden.
- [Tauri platform design](doc/design/TAURI_PLATFORM_DESIGN.md) — Tauri 2.0 candidate with a Rust client boundary.
- [Capacitor and Electron platform design](doc/design/CAPACITOR_ELECTRON_PLATFORM_DESIGN.md) — Capacitor for Android and iOS plus Electron for Windows and macOS.
- [Platform scheme Frequently Asked Questions](doc/design/PLATFORM_OPTIONS_FAQ.md) — reasons Valdi, .NET Multi-platform App UI, Flutter, and other options are not currently shortlisted.
