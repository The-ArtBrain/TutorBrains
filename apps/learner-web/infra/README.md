# Learner Web Infrastructure

This directory owns deployment mechanics and provider-specific infrastructure for `learner-web`. The application build remains provider-neutral; Cloudflare-specific code and policy stay here.

The current Cloudflare project is the Telugu Tutor course root, branded **TeluguTutorBrains** and identified by the Cloudflare-compatible lowercase slug `telugututorbrains`. It is not a shared container for every TutorBrains course. Each independent course gets its own deployment root; when its product boundary warrants it, that root becomes a separately owned application rather than a subdirectory of this deployment.

There is currently **no deployment triggered by a Git commit or pull request**. Production and preview deployments are explicit operator actions performed with [`deploy-cloudflare-pages.sh`](deploy-cloudflare-pages.sh).

## Ownership

This directory is the intended home for:

```text
infra/
├── .dockerignore
├── README.md
├── compose.yaml
├── Dockerfile.wrangler
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
    -> local unit and browser tests
    -> clean English and Hindi build
    -> policy staging
    -> explicit Wrangler upload from an isolated container
    -> Cloudflare Pages immutable deployment
```

GitHub stores source history but does not build or deploy the site in this phase. Cloudflare receives only the generated `apps/learner-web/dist/` output plus any Functions discovered under `infra/functions/`.

The Pages project should be created as a Direct Upload project. Cloudflare does not allow a Direct Upload project to be converted later to its native Git integration. Future automation can still use GitHub Actions or another continuous-integration service to invoke Wrangler against the same project. Deployment implementation and policy should remain here; a minimal provider-required trigger file may live outside `infra/` only when the provider cannot discover it here.

## Prerequisites

### One-time setup

Complete these steps once on each deployment machine:

1. Prepare the learner-web Python environment as described in [`../build-tools/README.md`](../build-tools/README.md).
2. Install the learner-web end-to-end test dependencies and Playwright browser described in [`../../../tests/end-to-end/learner-web/README.md`](../../../tests/end-to-end/learner-web/README.md).
3. Install Docker with Docker Compose v2.
4. Build the reviewed Wrangler container from the repository root:

   ```sh
   docker compose -f apps/learner-web/infra/compose.yaml build --pull wrangler
   docker compose -f apps/learner-web/infra/compose.yaml run --rm wrangler --version
   ```

   The version check prints the stable Wrangler release selected by npm's `latest` distribution tag when the image was built. Review `Dockerfile.wrangler`, the reported version, and the test results before using a rebuilt image. Wrangler and its Node.js dependencies remain inside the `tutorbrains-wrangler:stable` image. The container mounts the repository read-only and uses a temporary home directory. The deployment script refuses to build or refresh this image implicitly during preview or production.

   Rebuild with `--pull --no-cache` whenever checking for a newer stable Wrangler release. A breaking change then appears during the explicit rebuild and verification step, where the repository scripts or configuration can be upgraded before deployment:

   ```sh
   docker compose -f apps/learner-web/infra/compose.yaml build --pull --no-cache wrangler
   docker compose -f apps/learner-web/infra/compose.yaml run --rm wrangler --version
   ```
5. Create a restricted Cloudflare API token with Account > Cloudflare Pages > Edit permission. Store the token and account identifier in an approved secret store; never place them in Git, `.dev.vars`, shell history, or a checked-in environment file.
6. Create the Pages project once, if it does not already exist. Export the credentials into the current shell first, as shown in the per-deployment checklist below, then run:

   ```sh
   docker compose -f apps/learner-web/infra/compose.yaml run --rm wrangler \
     pages project create telugututorbrains --production-branch main
   ```

### Before every deployment

Complete these checks before running `deploy-cloudflare-pages.sh preview` or `deploy-cloudflare-pages.sh production`:

1. Start Docker and confirm Docker Compose v2 is available:

   ```sh
   docker compose version
   ```

2. From the repository root, confirm that the reviewed Wrangler image exists and inspect its version:

   ```sh
   docker image inspect tutorbrains-wrangler:stable >/dev/null
   docker compose -f apps/learner-web/infra/compose.yaml run --rm wrangler --version
   ```

3. Export the restricted Cloudflare credentials into the current shell:

   ```sh
   export CLOUDFLARE_ACCOUNT_ID="..."
   export CLOUDFLARE_API_TOKEN="..."
   ```

4. Confirm the intended Git revision is committed and the worktree is clean:

   ```sh
   git status --short
   git rev-parse --short HEAD
   ```

   `git status --short` must produce no output. The deployment script rejects a dirty worktree so the uploaded artifact remains traceable to the recorded commit.

5. Confirm the target: use a non-production branch label for a preview, or verify that the production destination is exactly `learntelugu.brainos.in`.

Use a Cloudflare API token limited to the required account and Cloudflare Pages edit permission. Rotate or revoke it according to the account's credential policy.

## Commands

Run these commands from `apps/learner-web` or use the script by absolute path.

Build and verify without contacting Cloudflare:

```sh
./infra/deploy-cloudflare-pages.sh build
```

Create a preview deployment for an explicit non-production branch label:

```sh
./infra/deploy-cloudflare-pages.sh preview manual-review
```

Deploy to the production branch only after reviewing the generated output:

```sh
./infra/deploy-cloudflare-pages.sh production --confirm learntelugu.brainos.in
```

The production confirmation is intentionally exact and case-sensitive. Both preview and production deployments require a clean Git worktree so the uploaded artifact can be traced to the attached commit SHA.

Defaults can be changed for an intentional migration:

```sh
CLOUDFLARE_PAGES_PROJECT="another-project" \
CLOUDFLARE_PRODUCTION_BRANCH="release" \
./infra/deploy-cloudflare-pages.sh production --confirm learntelugu.brainos.in
```

Changing these values is an operational decision and should be recorded with the release.

## What the script does

For every command, the script:

1. verifies required local tools and dependencies;
2. runs the Python build-tool unit tests;
3. runs the learner-web Playwright suite;
4. deletes only the generated learner-web `dist/` directory;
5. builds English and Hindi outputs;
6. stages recognized Cloudflare policy artifacts, if present; and
7. verifies the expected root and locale entry pages.

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
