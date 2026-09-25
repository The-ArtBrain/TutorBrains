# Learner Web Infrastructure

This directory owns deployment mechanics and provider-specific infrastructure for `learner-web`. The application build remains provider-neutral; Cloudflare-specific code and policy stay here.

There is currently **no deployment triggered by a Git commit or pull request**. Production and preview deployments are explicit operator actions performed with [`deploy-cloudflare-pages.sh`](deploy-cloudflare-pages.sh).

## Ownership

This directory is the intended home for:

```text
infra/
├── README.md
├── deploy-cloudflare-pages.sh
├── functions/                 # Cloudflare Pages Functions, when implemented
├── policies/                  # _headers, _redirects, and _routes.json sources
└── wrangler.jsonc             # downloaded/reviewed Pages configuration, when needed
```

Do not create empty directories merely to reserve these names. Add each directory when it owns a real artifact.

Cloudflare requires a Pages `functions/` directory to be at the root from which Wrangler runs, rather than inside the published `dist/` directory. The deployment script runs Wrangler from `infra/`, so future JavaScript Functions belong in `infra/functions/` and are discovered without moving them into application source or generated output.

Policy files belong in `infra/policies/`. Before deployment, the script copies these recognized files into the generated `dist/` root when they exist:

- `_headers`
- `_redirects`
- `_routes.json`

The deployment fails if a future policy-copy step cannot produce a complete output. `dist/` remains generated and must not be committed.

## Release model

The current release model is manual Direct Upload:

```text
operator command
    -> local unit and browser tests
    -> clean English and Hindi build
    -> policy staging
    -> explicit Wrangler upload
    -> Cloudflare Pages immutable deployment
```

GitHub stores source history but does not build or deploy the site in this phase. Cloudflare receives only the generated `apps/learner-web/dist/` output plus any Functions discovered under `infra/functions/`.

The Pages project should be created as a Direct Upload project. Cloudflare does not allow a Direct Upload project to be converted later to its native Git integration. Future automation can still use GitHub Actions or another continuous-integration service to invoke Wrangler against the same project. Deployment implementation and policy should remain here; a minimal provider-required trigger file may live outside `infra/` only when the provider cannot discover it here.

## Prerequisites

Before running the script:

1. Prepare the learner-web Python environment as described in [`../build-tools/README.md`](../build-tools/README.md).
2. Install the learner-web end-to-end test dependencies and Playwright browser described in [`../../../tests/end-to-end/learner-web/README.md`](../../../tests/end-to-end/learner-web/README.md).
3. Install a reviewed, pinned Wrangler version so `npx --no-install wrangler` succeeds. The script deliberately does not download an unpinned CLI during a release.
4. Authenticate Wrangler locally with `npx wrangler login`, or export restricted credentials:

   ```sh
   export CLOUDFLARE_ACCOUNT_ID="..."
   export CLOUDFLARE_API_TOKEN="..."
   ```

5. Create the Pages project once, if it does not already exist:

   ```sh
   npx wrangler pages project create tutorbrains-courses --production-branch main
   ```

Use a Cloudflare API token limited to the required account and Cloudflare Pages edit permission. Never place tokens, account credentials, `.dev.vars`, or local Wrangler state in Git.

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

`build` stops at that point. `preview` and `production` then run Wrangler from `infra/`, allowing future `infra/functions/` code to be included in the Pages deployment.

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
4. invoke this script or an equivalent `infra/` entry point with pinned tools;
5. attach the commit SHA to the Pages deployment; and
6. run post-deployment smoke tests against `https://learntelugu.brainos.in`.

See [Cloudflare Pages hosting and DNS specification](../../../doc/design/CLOUDFLARE_PAGES_HOSTING_SPEC.md) for DNS, domain, verification, and rollback requirements.
