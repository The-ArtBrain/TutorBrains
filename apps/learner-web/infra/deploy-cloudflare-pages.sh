#!/usr/bin/env bash

set -euo pipefail

readonly INFRA_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly APP_ROOT="$(cd "${INFRA_ROOT}/.." && pwd)"
readonly REPOSITORY_ROOT="$(cd "${APP_ROOT}/../.." && pwd)"
readonly DIST_ROOT="${APP_ROOT}/dist"
readonly BUILD_PYTHON="${APP_ROOT}/build-tools/.venv/bin/python"
readonly BUILD_SCRIPT="${APP_ROOT}/build-tools/build.py"
readonly BUILD_TEST_ROOT="${APP_ROOT}/build-tools/tests"
readonly E2E_ROOT="${REPOSITORY_ROOT}/tests/end-to-end/learner-web"
readonly POLICY_ROOT="${INFRA_ROOT}/policies"
readonly COMPOSE_FILE="${INFRA_ROOT}/compose.yaml"
readonly WRANGLER_IMAGE="tutorbrains-wrangler:stable"
readonly PAGES_PROJECT="${CLOUDFLARE_PAGES_PROJECT:-telugututorbrains}"
readonly PRODUCTION_BRANCH="${CLOUDFLARE_PRODUCTION_BRANCH:-main}"
readonly PRODUCTION_HOST="learntelugu.brainos.in"

usage() {
  cat <<'EOF'
Usage:
  deploy-cloudflare-pages.sh build
  deploy-cloudflare-pages.sh preview <branch-label>
  deploy-cloudflare-pages.sh production --confirm learntelugu.brainos.in

Commands:
  build       Run tests and create a clean dist/ without contacting Cloudflare.
  preview     Build, then explicitly upload a non-production preview deployment.
  production  Build, then upload to the configured production branch. Requires
              the exact confirmation shown above.

Optional environment variables:
  CLOUDFLARE_PAGES_PROJECT       Pages project identifier (default: telugututorbrains)
  CLOUDFLARE_PRODUCTION_BRANCH   Pages production branch (default: main)
  CLOUDFLARE_ACCOUNT_ID          Used by Wrangler when authenticating with a token
  CLOUDFLARE_API_TOKEN           Restricted Cloudflare Pages API token
EOF
}

fail() {
  printf 'Error: %s\n' "$*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"
}

run_wrangler() {
  docker compose -f "${COMPOSE_FILE}" run --rm --no-deps wrangler "$@"
}

require_wrangler_container() {
  require_command docker
  docker compose version >/dev/null 2>&1 || fail "Docker Compose v2 is required."
  docker image inspect "${WRANGLER_IMAGE}" >/dev/null 2>&1 || fail \
    "Wrangler container missing. Build it with: docker compose -f apps/learner-web/infra/compose.yaml build wrangler"

  local version
  version="$(run_wrangler --version)"
  [[ -n "${version}" ]] || fail "Wrangler in ${WRANGLER_IMAGE} did not report a version."
}

require_clean_worktree() {
  if [[ -n "$(git -C "${REPOSITORY_ROOT}" status --porcelain)" ]]; then
    fail "Deployment requires a clean Git worktree so the artifact matches its commit."
  fi
}

stage_policies() {
  [[ -d "${POLICY_ROOT}" ]] || fail "Missing Cloudflare policy directory: ${POLICY_ROOT}"

  local required_policy
  for required_policy in _headers _routes.json; do
    [[ -f "${POLICY_ROOT}/${required_policy}" ]] || fail "Missing required Cloudflare policy: ${required_policy}"
  done

  local policy
  for policy in _headers _redirects _routes.json; do
    if [[ -f "${POLICY_ROOT}/${policy}" ]]; then
      cp "${POLICY_ROOT}/${policy}" "${DIST_ROOT}/${policy}"
    fi
  done
}

build_and_verify() {
  [[ -x "${BUILD_PYTHON}" ]] || fail "Build environment missing. Follow apps/learner-web/build-tools/README.md."
  [[ -d "${E2E_ROOT}/node_modules/@playwright/test" ]] || fail "Playwright dependencies missing. Follow tests/end-to-end/learner-web/README.md."

  "${BUILD_PYTHON}" -m unittest discover -s "${BUILD_TEST_ROOT}" -v
  npm --prefix "${E2E_ROOT}" test

  "${BUILD_PYTHON}" "${BUILD_SCRIPT}" clean
  "${BUILD_PYTHON}" "${BUILD_SCRIPT}"
  "${BUILD_PYTHON}" "${BUILD_SCRIPT}" --instruction-language hi

  stage_policies

  [[ -f "${DIST_ROOT}/index.html" ]] || fail "Missing generated root entry: dist/index.html"
  [[ -f "${DIST_ROOT}/en/index.html" ]] || fail "Missing generated English entry: dist/en/index.html"
  [[ -f "${DIST_ROOT}/hi/index.html" ]] || fail "Missing generated Hindi entry: dist/hi/index.html"
  [[ -f "${DIST_ROOT}/_headers" ]] || fail "Missing staged Cloudflare headers: dist/_headers"
  [[ -f "${DIST_ROOT}/_routes.json" ]] || fail "Missing staged Cloudflare routes: dist/_routes.json"
}

deploy() {
  local branch="$1"
  local commit_hash
  local commit_message

  require_wrangler_container

  commit_hash="$(git -C "${REPOSITORY_ROOT}" rev-parse HEAD)"
  commit_message="$(git -C "${REPOSITORY_ROOT}" log -1 --pretty=%s)"

  run_wrangler pages deploy "/workspace/apps/learner-web/dist" \
    --project-name "${PAGES_PROJECT}" \
    --branch "${branch}" \
    --commit-hash "${commit_hash}" \
    --commit-message "${commit_message}"
}

main() {
  local command_name="${1:-}"

  require_command git
  require_command npm

  case "${command_name}" in
    build)
      [[ $# -eq 1 ]] || { usage >&2; exit 2; }
      build_and_verify
      printf 'Verified deployment artifact: %s\n' "${DIST_ROOT}"
      ;;
    preview)
      [[ $# -eq 2 ]] || { usage >&2; exit 2; }
      local preview_branch="$2"
      [[ "${preview_branch}" =~ ^[A-Za-z0-9._/-]+$ ]] || fail "Invalid preview branch label: ${preview_branch}"
      [[ "${preview_branch}" != "${PRODUCTION_BRANCH}" ]] || fail "Preview branch must not equal production branch ${PRODUCTION_BRANCH}."
      require_clean_worktree
      build_and_verify
      deploy "${preview_branch}"
      ;;
    production)
      [[ $# -eq 3 && "$2" == "--confirm" && "$3" == "${PRODUCTION_HOST}" ]] || { usage >&2; exit 2; }
      require_clean_worktree
      build_and_verify
      deploy "${PRODUCTION_BRANCH}"
      ;;
    -h|--help|help)
      usage
      ;;
    *)
      usage >&2
      exit 2
      ;;
  esac
}

main "$@"
