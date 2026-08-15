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
        └── student_onboarding_guide.md
```

## Directory Purpose

- `doc/` contains project documentation.
- `doc/spec/` contains product specifications and product requirements documents (PRDs).
- `characters_spec.md` defines the chapter-neutral model for independently accessible Telugu script units; chapters own the lesson links.
- `common_spec.md` defines tutor behaviour and product requirements inherited by every chapter.
- `grammar_spec.md` defines the chapter-neutral model for independently accessible grammar and usage units; chapters own the lesson links.
- `CHAPTER_01_TUTOR_PRD.md` defines the tutor product requirements driven by the Chapter 01 lesson specification.
- `capability_matrix.md` defines the technology-neutral product capabilities and ability-based authorization model.
- `student_onboarding_guide.md` defines the student journey before Chapter 01 and maps each action to the capability catalogue.

Update this file when the project structure or the purpose of a directory changes.
