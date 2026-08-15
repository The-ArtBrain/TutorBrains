# Telugu Vocabulary Unit Specification

**Status:** Draft  
**Scope:** Independently accessible Telugu vocabulary learning units

## 1. Purpose

This specification defines the shared model for Telugu vocabulary units that can be referenced from any lesson in any chapter.

This document does not assign vocabulary to chapters or lessons. Each chapter or lesson owns its teaching relationship, contextual examples, activities, evidence requirements, and progression decisions.

Vocabulary units must support any product instruction language. The canonical Telugu vocabulary remains unchanged, while meanings, explanations, pronunciation guidance, and transliteration may vary with the selected instruction language and its writing system. English and Roman-script values are defaults, not canonical substitutes for localized values.

## 2. Unit model

A vocabulary unit represents one independently teachable lexical item, such as a word, fixed expression, or other meaning-bearing form. A unit must:

- have a stable identifier that does not depend on a course, chapter, or lesson number;
- be directly retrievable using that identifier;
- describe one coherent vocabulary object;
- be reusable from multiple cards and lessons without duplicating its canonical definition; and
- contain no learner-specific or chapter-specific progression state.

Vocabulary units can be atomic or composite. A composite vocabulary unit is independently accessible under its own stable identifier and references its ordered component units plus the relationship that combines them. A fixed expression may therefore be taught as one vocabulary unit while its component words remain independently accessible.

When a vocabulary unit is independently presented, the platform uses a Card that references the unit. **Vocabulary Card** is descriptive shorthand, not a Card subtype or inheritance relationship. The vocabulary unit remains the canonical content identity; the Card owns presentation properties and explicitly granted technical abilities.

The storage format and access mechanism are not yet decided. A unit may later be represented as an individual file, structured data record, content-management object, or application resource, provided its stable identifier remains resolvable.

## 3. Provisional identity scheme

Until the vocabulary model is finalised, proposed identifiers use these prefixes:

- `VOC-WORD-*` for independently meaningful words;
- `VOC-EXPR-*` for fixed or conventional expressions; and
- `VOC-COMP-*` for other composite vocabulary forms.

Identifiers are provisional until the vocabulary taxonomy is validated. Course, chapter, lesson, sentence, and card definitions should reference the identifiers consistently once assigned.

## 4. Unit properties to determine

The exact property set is intentionally undecided. Product and curriculum design must determine whether a vocabulary unit needs properties such as:

- canonical Telugu form and normalized search form;
- vocabulary category and communicative purpose;
- instruction-language-specific meaning, explanation, pronunciation approximation, and transliteration;
- natural and slow pronunciation audio;
- whether the unit is atomic or composite and, for a composite, its ordered component references;
- character-unit and grammar-unit references;
- common inflected or spoken variants without treating every surface form as the same unit;
- register, politeness, social context, dialect, and usage constraints;
- related, contrasting, or easily confused vocabulary;
- sentence-unit examples independent of any one lesson;
- authored image, illustration, or other media references;
- accessibility metadata;
- assessment affordances; and
- language-review status and version.

These are candidates, not approved storage fields.

## 5. Composition and referencing requirements

- A card, sentence, chapter, or lesson references a vocabulary unit by stable identifier.
- A Card presenting vocabulary references its vocabulary unit rather than copying the unit definition.
- The referring lesson owns whether the vocabulary is introduced, recognised, imitated, adapted, created, reviewed, or assessed.
- The referring card owns its reveal order, interaction, media arrangement, prompt level, and evidence request.
- A vocabulary unit must not contain backlinks or progression state for a particular card, lesson, or chapter.
- Composite vocabulary units reference their components by stable identifier and preserve component order where order carries meaning.
- A sentence unit may reference vocabulary units while retaining its own identity as a concrete utterance.
- Updating a vocabulary unit must not silently change the intended learning outcome of a card or lesson that references an earlier approved version.

## 6. Open decisions

- What distinguishes a reusable fixed expression from a sentence unit?
- Which inflected forms require distinct vocabulary identities, and which remain variants?
- Which properties are required for every vocabulary unit, and which depend on unit type?
- How should variants, dialect forms, synonyms, opposites, and related words be represented?
- How should tokenization and component order work for Telugu forms whose written boundaries do not map cleanly to instruction-language words?
- How should versioning protect cards, sentences, and lessons when a vocabulary unit changes?
- Which identifiers are suitable for long-term content and application interfaces?
