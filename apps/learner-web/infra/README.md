# Learner Web Infrastructure

This directory owns deployment mechanics and provider-specific infrastructure for `learner-web`. The application build remains provider-neutral; Cloudflare-specific code and policy stay here.

The current Cloudflare project is the Telugu Tutor course root, branded **TeluguTutorBrains** and identified by the Cloudflare-compatible lowercase slug `telugututorbrains`. It is not a shared container for every TutorBrains course. Each independent course gets its own deployment root; when its product boundary warrants it, that root becomes a separately owned application rather than a subdirectory of this deployment.

There is currently **no deployment triggered by a Git commit or pull request**. Production and preview deployments are explicit operator actions performed with [`deploy-cloudflare-pages.sh`](deploy-cloudflare-pages.sh).

## Ownership

This directory is the intended home for:

```text
infra/
├── README.md
├── compose.yaml
├── Dockerfile.wrangler
├── Dockerfile.wrangler.dockerignore
├── container-build.sh
├── deploy-cloudflare-pages.sh
├── functions/                 # Cloudflare Pages Functions
├── policies/                  # _headers, optional _redirects, and _routes.json sources
└── wrangler.jsonc             # downloaded/reviewed Pages configuration, when needed
```

Do not create empty directories merely to reserve these names. Add each directory when it owns a real artifact.

Cloudflare requires a Pages `functions/` directory to be at the root from which Wrangler runs, rather than inside the published `dist/` directory. The container runs Wrangler from `infra/`, so the root Function in `infra/functions/` is discovered without moving it into application source or generated output.

Policy files belong in `infra/policies/`. Before deployment, the script copies these recognized files into the generated `dist/` root when they exist:

- `_headers`
- `_redirects`
- `_routes.json`

The deployment fails unless `_headers` and `_routes.json` produce a complete output. `_redirects` remains optional. `dist/` remains generated and must not be committed.

## Release model

The current release model is manual Direct Upload:

```text
operator command
    -> Docker CLI runs the complete test, auth-bundle, site-build, policy-staging, and artifact-verification pipeline in the existing container
    -> explicit Wrangler upload from that container
    -> Cloudflare Pages immutable deployment
```

The host runs only the deployment shell script and Docker CLI. Git checks and commit metadata, Python, npm, Playwright, content generation, policy staging, and Wrangler all run in the persistent container. No host Git, Python environment, npm install, or browser installation is required for this workflow. The container receives the repository read-only and writes generated output only through the learner-web `dist/` mount.

GitHub stores source history but does not build or deploy the site in this phase. Cloudflare receives only the selected generated root, `apps/learner-web/dist/<root>/`, plus any Functions discovered under `infra/functions/`. The default root is `telugu`; the parent `dist/` directory is never uploaded.

The Pages project should be created as a Direct Upload project. Cloudflare does not allow a Direct Upload project to be converted later to its native Git integration. Future automation can still use GitHub Actions or another continuous-integration service to invoke Wrangler against the same project. Deployment implementation and policy should remain here; a minimal provider-required trigger file may live outside `infra/` only when the provider cannot discover it here.

## Prerequisites

### One-time setup

Complete these steps once on each deployment machine:

1. Install Docker with Docker Compose v2. Host Python, npm, and Playwright are not used by this deploy workflow.
2. Build the complete test/build/Wrangler image from the repository root:

   ```sh
   docker compose -f apps/learner-web/infra/compose.yaml build --pull wrangler
   ```

   The image installs the pinned auth and Playwright npm dependencies, Google Chrome Stable for the container architecture (`amd64` or `arm64`), and uv, in addition to Wrangler. Playwright's bundled `install chrome` command currently rejects Linux ARM64, so the Dockerfile installs Google's architecture-specific Chrome package directly at the path used by the `chrome` channel. The Playwright test package is resolved from the image's pinned install even when the read-only source mount contains host `node_modules`. It copies the learner-web build-tools `pyproject.toml` and runs `uv sync`; Python compatibility and the build dependency are defined there, with no Python version duplicated in the Dockerfile. A `uv.lock` is not tracked in Git, so uv resolves dependencies from the project definition during the image build. Review `Dockerfile.wrangler` and run the full verification before using a rebuilt image. The deployment helper runs both test suites, cleans/builds the shared auth bundle, generates English and Hindi site output, stages Cloudflare policies, and verifies the final artifact inside that container. The repository stays read-only except for the learner-web `dist/` output mount and temporary dependency overlay, where generated files are written. The persistent container defaults to the Pages project name (`telugututorbrains`) and can be overridden with `CLOUDFLARE_WRANGLER_CONTAINER`. The deployment script only uses an already-running named container: it does not create or start one, and fails if it is missing or stopped.

   On a new setup only, create the persistent container once after building the image. Skip this if your existing container is already configured and running:

   ```sh
   docker compose -f apps/learner-web/infra/compose.yaml run --detach --no-deps \
     --name telugututorbrains --entrypoint /bin/sh wrangler \
     -c 'while :; do sleep 3600; done'
   docker exec telugututorbrains wrangler --version
   ```

   This is a one-time manual container creation, not something the deployment script runs. Rebuilding the image does not update an existing container, and changing Compose mounts requires creating a container with the updated configuration. If your current container predates the Chrome or temporary npm overlay setup, explicitly create a second persistent container with a different name, then use that name for each deployment:

   ```sh
   docker compose -f apps/learner-web/infra/compose.yaml run --detach --no-deps \
     --name telugututorbrains-auth --entrypoint /bin/sh wrangler \
     -c 'while :; do sleep 3600; done'
   CLOUDFLARE_WRANGLER_CONTAINER=telugututorbrains-auth \
     ./apps/learner-web/infra/deploy-cloudflare-pages.sh build
   ```

   Rebuild with `--pull --no-cache` whenever checking for a newer stable Wrangler release or changing the npm build dependencies/build script. The npm layer is reinstalled from its checked-in lockfile; a breaking change then appears during explicit rebuild and verification before deployment:

   ```sh
   docker compose -f apps/learner-web/infra/compose.yaml build --pull --no-cache wrangler
   docker exec "${CLOUDFLARE_WRANGLER_CONTAINER:-telugututorbrains}" wrangler --version
   ```
3. Create a restricted Cloudflare API token with Account > Cloudflare Pages > Edit permission. Store the token and account identifier in an approved secret store; never place them in Git, `.dev.vars`, shell history, or a checked-in environment file.
4. Create the Pages project once, if it does not already exist. Export the credentials into the current shell first, as shown in the per-deployment checklist below, then run:

   ```sh
   docker exec \
     --env "CLOUDFLARE_ACCOUNT_ID=${CLOUDFLARE_ACCOUNT_ID}" \
     --env "CLOUDFLARE_API_TOKEN=${CLOUDFLARE_API_TOKEN}" \
     "${CLOUDFLARE_WRANGLER_CONTAINER:-telugututorbrains}" \
     wrangler pages project create telugututorbrains --production-branch main
   ```

### Before every deployment

Complete these checks from the repository root before running `apps/learner-web/infra/deploy-cloudflare-pages.sh preview` or `apps/learner-web/infra/deploy-cloudflare-pages.sh production`:

1. Start Docker and confirm Docker Compose v2 is available:

   ```sh
   docker compose version
   ```

2. From the repository root, confirm that the reviewed image and selected running container exist, then inspect its version:

   ```sh
   docker image inspect tutorbrains-wrangler:stable >/dev/null
   docker container inspect "${CLOUDFLARE_WRANGLER_CONTAINER:-telugututorbrains}" >/dev/null
   docker exec "${CLOUDFLARE_WRANGLER_CONTAINER:-telugututorbrains}" wrangler --version
   ```

3. Export the restricted Cloudflare credentials into the current shell:

   ```sh
   export CLOUDFLARE_ACCOUNT_ID="..."
   export CLOUDFLARE_API_TOKEN="..."
   ```

   Optionally enable Firebase auth in the generated site by setting `BRAINOS_FIREBASE_CONFIG` to a repository-relative config path, for example `apps/learner-web/auth/firebase-config.telugu.local.json`. The config must be inside the repository so the container can read it. Without it, the bundle is built but authentication remains disabled in the generated pages.

4. Confirm the intended Git revision is committed and the worktree is clean inside the selected container:

   ```sh
   docker exec "${CLOUDFLARE_WRANGLER_CONTAINER:-telugututorbrains}" git -C /workspace status --short
   docker exec "${CLOUDFLARE_WRANGLER_CONTAINER:-telugututorbrains}" git -C /workspace rev-parse --short HEAD
   ```

   `git status --short` must produce no output. The deployment script rejects a dirty worktree so the uploaded artifact remains traceable to the recorded commit.

5. Confirm the current Git branch and target. Pass the current branch name to the preview command. Production defaults to `main`; when deploying another configured production branch, pass it explicitly with `--branch`. Also verify that the production destination is exactly `learntelugu.brainos.in`.

Use a Cloudflare API token limited to the required account and Cloudflare Pages edit permission. Rotate or revoke it according to the account's credential policy.

## Commands

Run every command in this section from the repository root.

Build and verify without contacting Cloudflare:

```sh
./apps/learner-web/infra/deploy-cloudflare-pages.sh build
```

The default root is `telugu`. Select another independently deployable root explicitly:

```sh
./apps/learner-web/infra/deploy-cloudflare-pages.sh build --root another-course
```

Create a preview deployment for an explicit non-production branch label:

```sh
./apps/learner-web/infra/deploy-cloudflare-pages.sh preview \
  "$(docker exec "${CLOUDFLARE_WRANGLER_CONTAINER:-telugututorbrains}" git -C /workspace branch --show-current)"
```

Test uncommitted work in an isolated Cloudflare preview deployment:

```sh
./apps/learner-web/infra/deploy-cloudflare-pages.sh preview-uncommitted manual-test
```

`preview-uncommitted` accepts a non-production preview label rather than requiring a real Git branch. It runs the complete test and build pipeline, attaches the current `HEAD` commit for context, marks the deployment as having a dirty worktree, and never accepts the production label `main`. Use a distinct label when separate uncommitted previews must remain independently addressable.

Deploy to the production branch only after reviewing the generated output:

```sh
./apps/learner-web/infra/deploy-cloudflare-pages.sh production --confirm learntelugu.brainos.in
```

Every command accepts `--root <name>`. The script builds `dist/<name>/` and uploads only that directory. For example:

```sh
./apps/learner-web/infra/deploy-cloudflare-pages.sh preview-uncommitted manual-test --root telugu
```

`main` is the default production Git branch. Supply another branch explicitly only when it is also configured as the Cloudflare Pages production branch:

```sh
./apps/learner-web/infra/deploy-cloudflare-pages.sh production \
  --branch release \
  --confirm learntelugu.brainos.in
```

The supplied branch must match the currently checked-out Git branch. The production confirmation is intentionally exact and case-sensitive. Both preview and production deployments require a clean Git worktree so the uploaded artifact can be traced to the attached commit SHA.

Defaults can be changed for an intentional migration:

```sh
CLOUDFLARE_PAGES_PROJECT="another-project" \
./apps/learner-web/infra/deploy-cloudflare-pages.sh production \
  --branch release \
  --confirm learntelugu.brainos.in
```

Changing these values is an operational decision and should be recorded with the release.

### Change the Cloudflare production branch

Wrangler accepts the production branch when the Direct Upload project is created:

```sh
docker exec \
  --env "CLOUDFLARE_ACCOUNT_ID=${CLOUDFLARE_ACCOUNT_ID}" \
  --env "CLOUDFLARE_API_TOKEN=${CLOUDFLARE_API_TOKEN}" \
  "${CLOUDFLARE_WRANGLER_CONTAINER:-telugututorbrains}" \
  wrangler \
  pages project create telugututorbrains --production-branch main
```

Wrangler does not currently provide a `pages project update` command. To change an existing Direct Upload project's stored production branch, use the Cloudflare Pages API:

```sh
curl --request PATCH \
  "https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/pages/projects/telugututorbrains" \
  --header "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{"production_branch":"release"}'
```

Replace `release` with the intended production branch label. This changes how Cloudflare classifies subsequent Direct Upload deployments; it does not connect the Pages project to Git or verify that the branch exists in a remote repository. The branch supplied to `deploy-cloudflare-pages.sh production --branch <git-branch>` must then use the same value.

## What the script does

For every command, the script:

1. checks that the selected persistent container already exists and is running; if not, it fails without creating or starting one;
2. runs tests, then cleans generated course outputs while preserving the `dist/` directory and shared mount point;
3. reuses the selected container, runs npm clean for `dist/auth.js`, and builds a fresh auth bundle directly into learner-web `dist/`;
4. builds English and Hindi outputs below the selected `dist/<root>/` directory, passing `BRAINOS_FIREBASE_CONFIG` when supplied;
5. stages recognized Cloudflare policy artifacts into that root; and
6. verifies the selected root and its locale entry pages.

`build` stops at that point. `preview` and `production` then run Wrangler from `infra/`, allowing the root Function under `infra/functions/` to be included in the Pages deployment.

The script does not:

- create or modify DNS records;
- attach a custom domain;
- create commits, tags, or releases;
- push to GitHub;
- deploy merely because a commit exists;
- install or upgrade dependencies; or
- store Cloudflare credentials.

## Future automation

If deployment automation is added later, it should call the same checked-in build and deployment entry point rather than duplicating commands in a provider dashboard. A controlled pipeline should:

1. build and test a specific commit;
2. retain the generated artifact and checksum;
3. require an explicit production approval;
4. invoke this script or an equivalent `infra/` entry point with the reviewed stable container;
5. attach the commit SHA to the Pages deployment; and
6. run post-deployment smoke tests against `https://learntelugu.brainos.in`.

See [Cloudflare Pages hosting and DNS specification](../../../doc/design/CLOUDFLARE_PAGES_HOSTING_SPEC.md) for DNS, domain, verification, and rollback requirements.
