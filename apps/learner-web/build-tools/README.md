# Learner Web build tool

Run the learner-web build from the repository root:

```sh
python3 apps/learner-web/build-tools/build.py
```

The build has two stages:

1. `generate_course_content` prepares course content. It is intentionally empty for now.
2. `fill_and_publish_html` will eventually fill HTML placeholders. For now, it copies the learner-web `html`, `css`, and `assets` directories unchanged into `apps/learner-web/dist/`.

The `dist/` directory is generated output and is not committed.
