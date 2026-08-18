# Project Memory

## Directory Structure

```text
TeluguTutorbrain/
├── README.md
├── memory.md
└── doc/
    └── spec/
        ├── CHAPTER_01_TUTOR_PRD.md
        ├── capability_matrix.md
        ├── characters_spec.md
        ├── common_spec.md
        ├── grammar_spec.md
        ├── platform_spec.md
        ├── sentence_spec.md
        ├── student_onboarding_guide.md
        └── vocabulary_spec.md
```

## Directory Purpose

- `doc/` contains project documentation.
- `doc/spec/` contains product specifications and product requirements documents (PRDs).
- `characters_spec.md` defines the chapter-neutral model for independently accessible Telugu script units; chapters own the lesson links.
- `common_spec.md` defines tutor behaviour and product requirements inherited by every chapter.
- `grammar_spec.md` defines the chapter-neutral model for independently accessible grammar and usage units; chapters own the lesson links.
- `CHAPTER_01_TUTOR_PRD.md` defines the tutor product requirements driven by the Chapter 01 lesson specification.
- `capability_matrix.md` defines the technology-neutral product capabilities and ability-based authorization model.
- `platform_spec.md` defines platform requirements, runtime boundaries, and platform-neutral presentation entities.
- `sentence_spec.md` defines the chapter-neutral model for independently accessible sentence units.
- `student_onboarding_guide.md` defines the student journey before Chapter 01 and maps each action to the capability catalogue.
- `vocabulary_spec.md` defines the chapter-neutral model for independently accessible vocabulary units.

## Working Conventions

- Understand the directory structure and the purpose of the relevant folders before adding, moving, or changing files.
- When work includes Artificial Intelligence (AI) assistance, provide appropriate attribution in the resulting commit or deliverable.

Update this file when the project structure or the purpose of a directory changes.
