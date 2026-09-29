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
readonly WRANGLER_STATE_ROOT="${INFRA_ROOT}/.wrangler"
readonly WRANGLER_IMAGE="tutorbrains-wrangler:stable"
readonly PAGES_PROJECT="${CLOUDFLARE_PAGES_PROJECT:-telugututorbrains}"
readonly DEFAULT_DISTRIBUTION_ROOT="telugu"
readonly DEFAULT_PRODUCTION_BRANCH="main"
readonly PRODUCTION_HOST="learntelugu.brainos.in"

usage() {
  cat <<'EOF'
Usage:
  deploy-cloudflare-pages.sh build [--root <name>]
  deploy-cloudflare-pages.sh preview <git-branch> [--root <name>]
  deploy-cloudflare-pages.sh preview-uncommitted <preview-label> [--root <name>]
  deploy-cloudflare-pages.sh production [--branch <git-branch>] [--root <name>] --confirm learntelugu.brainos.in

Commands:
  build       Run tests and create dist/<name>/ without contacting Cloudflare.
  preview     Build, then explicitly upload a non-production preview deployment.
  preview-uncommitted
              Build and upload a dirty-worktree preview under an explicit label.
  production  Build, then upload to the supplied Git branch (default: main).
              Requires the exact confirmation shown above.

Optional environment variables:
  CLOUDFLARE_PAGES_PROJECT       Pages project identifier (default: telugututorbrains)
  CLOUDFLARE_ACCOUNT_ID          Used by Wrangler when authenticating with a token
  CLOUDFLARE_API_TOKEN           Restricted Cloudflare Pages API token

Options:
  --root <name>                  Distribution folder below dist/ (default: telugu)
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
  ensure_wrangler_container
  docker exec \
    --env "CLOUDFLARE_ACCOUNT_ID=${CLOUDFLARE_ACCOUNT_ID:-}" \
    --env "CLOUDFLARE_API_TOKEN=${CLOUDFLARE_API_TOKEN:-}" \
    "${PAGES_PROJECT}" wrangler "$@"
}

ensure_wrangler_container() {
  mkdir -p "${WRANGLER_STATE_ROOT}"

  if docker container inspect "${PAGES_PROJECT}" >/dev/null 2>&1; then
    if [[ "$(docker container inspect --format '{{.State.Running}}' "${PAGES_PROJECT}")" != "true" ]]; then
      docker start "${PAGES_PROJECT}" >/dev/null
    fi
    return
  fi

  docker compose -f "${COMPOSE_FILE}" run --detach --no-deps \
    --name "${PAGES_PROJECT}" \
    --entrypoint /bin/sh \
    wrangler -c 'while :; do sleep 3600; done' >/dev/null
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

require_current_branch() {
  local requested_branch="$1"
  local current_branch

  git check-ref-format --branch "${requested_branch}" >/dev/null 2>&1 || fail "Invalid Git branch name: ${requested_branch}"
  current_branch="$(git -C "${REPOSITORY_ROOT}" branch --show-current)"
  [[ -n "${current_branch}" ]] || fail "Deployment is not allowed from a detached HEAD."
  [[ "${current_branch}" == "${requested_branch}" ]] || fail \
    "Requested branch ${requested_branch} does not match the current Git branch ${current_branch}."
}

validate_distribution_root() {
  local distribution_root="$1"
  [[ "${distribution_root}" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || fail \
    "Invalid distribution root ${distribution_root}; use a lowercase folder name with optional hyphens."
}

stage_policies() {
  local distribution_root="$1"
  local publish_root="${DIST_ROOT}/${distribution_root}"
  [[ -d "${POLICY_ROOT}" ]] || fail "Missing Cloudflare policy directory: ${POLICY_ROOT}"

  local required_policy
  for required_policy in _headers _routes.json; do
    [[ -f "${POLICY_ROOT}/${required_policy}" ]] || fail "Missing required Cloudflare policy: ${required_policy}"
  done

  local policy
  for policy in _headers _redirects _routes.json; do
    if [[ -f "${POLICY_ROOT}/${policy}" ]]; then
      cp "${POLICY_ROOT}/${policy}" "${publish_root}/${policy}"
    fi
  done
}

build_and_verify() {
  local distribution_root="$1"
  local publish_root="${DIST_ROOT}/${distribution_root}"
  [[ -x "${BUILD_PYTHON}" ]] || fail "Build environment missing. Follow apps/learner-web/build-tools/README.md."
  [[ -d "${E2E_ROOT}/node_modules/@playwright/test" ]] || fail "Playwright dependencies missing. Follow tests/end-to-end/learner-web/README.md."

  "${BUILD_PYTHON}" -m unittest discover -s "${BUILD_TEST_ROOT}" -v
  npm --prefix "${E2E_ROOT}" test

  "${BUILD_PYTHON}" "${BUILD_SCRIPT}" clean
  "${BUILD_PYTHON}" "${BUILD_SCRIPT}" --distribution-root "${distribution_root}"
  "${BUILD_PYTHON}" "${BUILD_SCRIPT}" --instruction-language hi --distribution-root "${distribution_root}"

  stage_policies "${distribution_root}"

  [[ -f "${publish_root}/index.html" ]] || fail "Missing generated root entry: dist/${distribution_root}/index.html"
  [[ -f "${publish_root}/en/index.html" ]] || fail "Missing generated English entry: dist/${distribution_root}/en/index.html"
  [[ -f "${publish_root}/hi/index.html" ]] || fail "Missing generated Hindi entry: dist/${distribution_root}/hi/index.html"
  [[ -f "${publish_root}/_headers" ]] || fail "Missing staged Cloudflare headers: dist/${distribution_root}/_headers"
  [[ -f "${publish_root}/_routes.json" ]] || fail "Missing staged Cloudflare routes: dist/${distribution_root}/_routes.json"
}

deploy() {
  local distribution_root="$1"
  local branch="$2"
  local commit_dirty="${3:-false}"
  local commit_hash
  local commit_message
  local -a deploy_arguments

  require_wrangler_container

  commit_hash="$(git -C "${REPOSITORY_ROOT}" rev-parse HEAD)"
  commit_message="$(git -C "${REPOSITORY_ROOT}" log -1 --pretty=%s)"

  deploy_arguments=(
    pages deploy "/workspace/apps/learner-web/dist/${distribution_root}"
    --project-name "${PAGES_PROJECT}"
    --branch "${branch}"
    --commit-hash "${commit_hash}"
    --commit-message "${commit_message}"
  )
  if [[ "${commit_dirty}" == "true" ]]; then
    deploy_arguments+=(--commit-dirty=true)
  fi

  run_wrangler "${deploy_arguments[@]}"
}

main() {
  local command_name="${1:-}"
  local distribution_root="${DEFAULT_DISTRIBUTION_ROOT}"

  require_command git
  require_command npm

  case "${command_name}" in
    build)
      if [[ $# -eq 3 && "$2" == "--root" ]]; then
        distribution_root="$3"
      elif [[ $# -ne 1 ]]; then
        usage >&2
        exit 2
      fi
      validate_distribution_root "${distribution_root}"
      build_and_verify "${distribution_root}"
      printf 'Verified deployment artifact: %s\n' "${DIST_ROOT}/${distribution_root}"
      ;;
    preview)
      if [[ $# -eq 4 && "$3" == "--root" ]]; then
        distribution_root="$4"
      elif [[ $# -ne 2 ]]; then
        usage >&2
        exit 2
      fi
      local preview_branch="$2"
      validate_distribution_root "${distribution_root}"
      require_current_branch "${preview_branch}"
      [[ "${preview_branch}" != "${DEFAULT_PRODUCTION_BRANCH}" ]] || fail "Preview branch must not equal production branch ${DEFAULT_PRODUCTION_BRANCH}."
      require_clean_worktree
      build_and_verify "${distribution_root}"
      deploy "${distribution_root}" "${preview_branch}"
      ;;
    preview-uncommitted)
      if [[ $# -eq 4 && "$3" == "--root" ]]; then
        distribution_root="$4"
      elif [[ $# -ne 2 ]]; then
        usage >&2
        exit 2
      fi
      local preview_label="$2"
      validate_distribution_root "${distribution_root}"
      git check-ref-format --branch "${preview_label}" >/dev/null 2>&1 || fail "Invalid preview label: ${preview_label}"
      [[ "${preview_label}" != "${DEFAULT_PRODUCTION_BRANCH}" ]] || fail "Uncommitted work cannot use the production branch label ${DEFAULT_PRODUCTION_BRANCH}."
      build_and_verify "${distribution_root}"
      deploy "${distribution_root}" "${preview_label}" true
      ;;
    production)
      local production_branch="${DEFAULT_PRODUCTION_BRANCH}"
      local confirmation=""
      shift
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --branch)
            [[ $# -ge 2 ]] || { usage >&2; exit 2; }
            production_branch="$2"
            shift 2
            ;;
          --confirm)
            [[ $# -ge 2 ]] || { usage >&2; exit 2; }
            confirmation="$2"
            shift 2
            ;;
          --root)
            [[ $# -ge 2 ]] || { usage >&2; exit 2; }
            distribution_root="$2"
            shift 2
            ;;
          *)
            usage >&2
            exit 2
            ;;
        esac
      done
      [[ "${confirmation}" == "${PRODUCTION_HOST}" ]] || { usage >&2; exit 2; }
      validate_distribution_root "${distribution_root}"
      require_current_branch "${production_branch}"
      require_clean_worktree
      build_and_verify "${distribution_root}"
      deploy "${distribution_root}" "${production_branch}"
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
