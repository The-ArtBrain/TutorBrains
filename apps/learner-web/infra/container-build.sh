#!/usr/bin/env bash

# Container-side build and verification entry point. The host deploy script
# invokes this file with `docker exec`; it runs only inside the existing
# Wrangler container.
#
# Arguments:
#   $1  distribution root, for example `telugu`
#   $2  optional Firebase config path inside the mounted repository, or empty
#
# Execution order (all commands below run inside this container):
#   /opt/brainos-build-venv/bin/python -m unittest discover -s /workspace/apps/learner-web/build-tools/tests -v
#   mkdir -p /workspace/tests/end-to-end/learner-web/node_modules/@playwright
#   ln -sfn /opt/brainos-e2e-review/node_modules/@playwright/test /workspace/tests/end-to-end/learner-web/node_modules/@playwright/test
#   LEARNER_WEB_PYTHON=/opt/brainos-build-venv/bin/python PLAYWRIGHT_OUTPUT_DIR=/tmp/learner-web-test-results npm --prefix /opt/brainos-e2e-review test -- --config /workspace/tests/end-to-end/learner-web/playwright.config.js
#   /opt/brainos-build-venv/bin/python /workspace/apps/learner-web/build-tools/build.py clean
#   BRAINOS_AUTH_ENTRY=/workspace/apps/learner-web/auth/src/main.js BRAINOS_AUTH_OUTFILE=/workspace/apps/learner-web/dist/auth.js npm --prefix /opt/brainos-auth-build run clean
#   BRAINOS_AUTH_ENTRY=/workspace/apps/learner-web/auth/src/main.js BRAINOS_AUTH_OUTFILE=/workspace/apps/learner-web/dist/auth.js npm --prefix /opt/brainos-auth-build run build
#   /opt/brainos-build-venv/bin/python /workspace/apps/learner-web/build-tools/build.py --distribution-root <root> [--firebase-config /workspace/<config>]
#   /opt/brainos-build-venv/bin/python /workspace/apps/learner-web/build-tools/build.py --instruction-language hi --distribution-root <root> [--firebase-config /workspace/<config>]
# Finally, available Cloudflare policies are copied to dist/<root>/ and the
# required deployment files are checked. `set -e` stops on the first failure.

set -euo pipefail

readonly REPOSITORY_ROOT="/workspace"
readonly APP_ROOT="${REPOSITORY_ROOT}/apps/learner-web"
readonly DIST_ROOT="${APP_ROOT}/dist"
readonly BUILD_PYTHON="/opt/brainos-build-venv/bin/python"
readonly BUILD_SCRIPT="${APP_ROOT}/build-tools/build.py"
readonly BUILD_TEST_ROOT="${APP_ROOT}/build-tools/tests"
readonly AUTH_NPM_ROOT="/opt/brainos-auth-build"
readonly AUTH_ENTRY="${APP_ROOT}/auth/src/main.js"
readonly E2E_NPM_ROOT="/opt/brainos-e2e-review"
readonly E2E_WORKSPACE_NODE_MODULES="${REPOSITORY_ROOT}/tests/end-to-end/learner-web/node_modules"
readonly E2E_CONFIG="${REPOSITORY_ROOT}/tests/end-to-end/learner-web/playwright.config.js"
readonly POLICY_ROOT="${APP_ROOT}/infra/policies"

fail() {
  printf 'Error: %s\n' "$*" >&2
  exit 1
}

distribution_root="${1:-}"
firebase_config_path="${2:-}"
[[ "${distribution_root}" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || fail \
  "Invalid distribution root '${distribution_root}'."

firebase_config_arguments=()
if [[ -n "${firebase_config_path}" ]]; then
  [[ "${firebase_config_path}" == /workspace/* ]] || fail \
    "Firebase config must resolve to a file under /workspace."
  [[ -f "${firebase_config_path}" ]] || fail "Firebase config not found: ${firebase_config_path}"
  firebase_config_arguments=(--firebase-config "${firebase_config_path}")
fi

[[ -x "${BUILD_PYTHON}" ]] || fail "Container Python build environment is missing."
[[ -x "${E2E_NPM_ROOT}/node_modules/.bin/playwright" ]] || fail "Container Playwright dependencies are missing."
[[ -x "${AUTH_NPM_ROOT}/node_modules/.bin/esbuild" ]] || fail "Container auth dependencies are missing."

"${BUILD_PYTHON}" -m unittest discover -s "${BUILD_TEST_ROOT}" -v
mkdir -p "${E2E_WORKSPACE_NODE_MODULES}/@playwright"
ln -sfn "${E2E_NPM_ROOT}/node_modules/@playwright/test" "${E2E_WORKSPACE_NODE_MODULES}/@playwright/test"
LEARNER_WEB_PYTHON="${BUILD_PYTHON}" \
PLAYWRIGHT_OUTPUT_DIR=/tmp/learner-web-test-results \
npm --prefix "${E2E_NPM_ROOT}" test -- --config "${E2E_CONFIG}"

"${BUILD_PYTHON}" "${BUILD_SCRIPT}" clean
BRAINOS_AUTH_ENTRY="${AUTH_ENTRY}" \
BRAINOS_AUTH_OUTFILE="${DIST_ROOT}/auth.js" \
npm --prefix "${AUTH_NPM_ROOT}" run clean
BRAINOS_AUTH_ENTRY="${AUTH_ENTRY}" \
BRAINOS_AUTH_OUTFILE="${DIST_ROOT}/auth.js" \
npm --prefix "${AUTH_NPM_ROOT}" run build

"${BUILD_PYTHON}" "${BUILD_SCRIPT}" --distribution-root "${distribution_root}" "${firebase_config_arguments[@]}"
"${BUILD_PYTHON}" "${BUILD_SCRIPT}" --instruction-language hi --distribution-root "${distribution_root}" "${firebase_config_arguments[@]}"

publish_root="${DIST_ROOT}/${distribution_root}"
[[ -d "${POLICY_ROOT}" ]] || fail "Missing Cloudflare policy directory: ${POLICY_ROOT}"
for policy in _headers _redirects _routes.json; do
  if [[ -f "${POLICY_ROOT}/${policy}" ]]; then
    cp "${POLICY_ROOT}/${policy}" "${publish_root}/${policy}"
  fi
done

for required in index.html en/index.html hi/index.html _headers _routes.json; do
  [[ -f "${publish_root}/${required}" ]] || fail "Missing generated deployment file: ${publish_root}/${required}"
done

printf 'Verified deployment artifact: %s\n' "${publish_root}"
