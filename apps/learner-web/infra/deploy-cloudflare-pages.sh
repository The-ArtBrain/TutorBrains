#!/usr/bin/env bash

set -euo pipefail

readonly INFRA_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly APP_ROOT="$(cd "${INFRA_ROOT}/.." && pwd)"
readonly REPOSITORY_ROOT="$(cd "${APP_ROOT}/../.." && pwd)"
readonly DIST_ROOT="${APP_ROOT}/dist"
readonly CONTAINER_BUILD_SCRIPT="/workspace/apps/learner-web/infra/container-build.sh"
readonly WRANGLER_IMAGE="tutorbrains-wrangler:stable"
readonly PAGES_PROJECT="${CLOUDFLARE_PAGES_PROJECT:-telugututorbrains}"
readonly WRANGLER_CONTAINER="${CLOUDFLARE_WRANGLER_CONTAINER:-${PAGES_PROJECT}}"
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
  CLOUDFLARE_WRANGLER_CONTAINER  Persistent Docker container name (defaults to project identifier)
  CLOUDFLARE_ACCOUNT_ID          Used by Wrangler when authenticating with a token
  CLOUDFLARE_API_TOKEN           Restricted Cloudflare Pages API token
  BRAINOS_FIREBASE_CONFIG        Optional course-local Firebase config path

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
  docker exec \
    --env "CLOUDFLARE_ACCOUNT_ID=${CLOUDFLARE_ACCOUNT_ID:-}" \
    --env "CLOUDFLARE_API_TOKEN=${CLOUDFLARE_API_TOKEN:-}" \
    "${WRANGLER_CONTAINER}" wrangler "$@"
}

container_git() {
  docker exec "${WRANGLER_CONTAINER}" git -C /workspace "$@"
}

require_wrangler_container() {
  require_command docker
  docker compose version >/dev/null 2>&1 || fail "Docker Compose v2 is required."
  docker image inspect "${WRANGLER_IMAGE}" >/dev/null 2>&1 || fail \
    "Wrangler container missing. Build it with: docker compose -f apps/learner-web/infra/compose.yaml build wrangler"

  docker container inspect "${WRANGLER_CONTAINER}" >/dev/null 2>&1 || fail \
    "Required persistent Docker container '${WRANGLER_CONTAINER}' is unavailable. This script will not create a container; create it explicitly using apps/learner-web/infra/README.md."
  [[ "$(docker container inspect --format '{{.State.Running}}' "${WRANGLER_CONTAINER}")" == "true" ]] || fail \
    "Required persistent Docker container '${WRANGLER_CONTAINER}' exists but is stopped. Start it explicitly, then retry."

  local version
  version="$(docker exec "${WRANGLER_CONTAINER}" wrangler --version)"
  [[ -n "${version}" ]] || fail "Wrangler in ${WRANGLER_IMAGE} did not report a version."

  docker exec "${WRANGLER_CONTAINER}" sh -c \
    "command -v git >/dev/null && command -v uv >/dev/null && test -x /opt/brainos-auth-build/node_modules/.bin/esbuild && test -f /opt/brainos-auth-build/clean.mjs && test -x /opt/brainos-e2e-review/node_modules/.bin/playwright && test -x /opt/brainos-build-venv/bin/python" || fail \
    "The existing Docker container does not have the complete build and test layers. Rebuild the image and explicitly create a fresh container as documented in apps/learner-web/infra/README.md."
}

require_clean_worktree() {
  if [[ -n "$(container_git status --porcelain)" ]]; then
    fail "Deployment requires a clean Git worktree so the artifact matches its commit."
  fi
}

require_current_branch() {
  local requested_branch="$1"
  local current_branch

  container_git check-ref-format --branch "${requested_branch}" >/dev/null 2>&1 || fail "Invalid Git branch name: ${requested_branch}"
  current_branch="$(container_git branch --show-current)"
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

# Build and test command details are documented in container-build.sh.
build_and_verify() {
  local distribution_root="$1"
  local firebase_config_path="${BRAINOS_FIREBASE_CONFIG:-}"
  local container_firebase_config=""
  require_wrangler_container

  if [[ -n "${firebase_config_path}" ]]; then
    if [[ "${firebase_config_path}" != /* ]]; then
      firebase_config_path="${REPOSITORY_ROOT}/${firebase_config_path}"
    fi
    [[ "${firebase_config_path}" == "${REPOSITORY_ROOT}/"* ]] || fail \
      "Firebase config must be inside the repository so the container can read it."
    container_firebase_config="/workspace/${firebase_config_path#"${REPOSITORY_ROOT}/"}"
  fi

  docker exec "${WRANGLER_CONTAINER}" bash "${CONTAINER_BUILD_SCRIPT}" \
    "${distribution_root}" "${container_firebase_config}"
}

build_auth_module() {
  docker exec \
    --env "BRAINOS_AUTH_ENTRY=/workspace/apps/learner-web/auth/src/main.js" \
    --env "BRAINOS_AUTH_OUTFILE=${AUTH_DOCKER_OUTPUT}" \
    "${WRANGLER_CONTAINER}" npm --prefix "${AUTH_DOCKER_ROOT}" run clean

  docker exec \
    --env "BRAINOS_AUTH_ENTRY=/workspace/apps/learner-web/auth/src/main.js" \
    --env "BRAINOS_AUTH_OUTFILE=${AUTH_DOCKER_OUTPUT}" \
    "${WRANGLER_CONTAINER}" npm --prefix "${AUTH_DOCKER_ROOT}" run build

  [[ -s "${AUTH_BUNDLE}" ]] || fail "The Docker npm build did not produce ${AUTH_BUNDLE}."
}

deploy() {
  local distribution_root="$1"
  local branch="$2"
  local commit_dirty="${3:-false}"
  local commit_hash
  local commit_message
  local -a deploy_arguments

  require_wrangler_container

  commit_hash="$(container_git rev-parse HEAD)"
  commit_message="$(container_git log -1 --pretty=%s)"

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
      require_wrangler_container
      container_git check-ref-format --branch "${preview_label}" >/dev/null 2>&1 || fail "Invalid preview label: ${preview_label}"
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
