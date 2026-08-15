# Telugu Sentence Unit Specification

**Status:** Draft  
**Scope:** Independently accessible Telugu sentence and utterance learning units

## 1. Purpose

This specification defines the shared model for concrete Telugu sentence and utterance units that can be referenced from any lesson in any chapter.

A sentence unit is a concrete learner-usable utterance. It is distinct from a grammar unit, which represents an abstract pattern, relationship, or usage concept, and from a vocabulary unit, which represents a lexical item or fixed expression.

This document does not assign sentences to chapters or lessons. Each chapter or lesson owns why a sentence appears, how it is taught, the acceptable contextual variants, its activity design, evidence requirements, and progression decisions.

Sentence units must support any product instruction language. Canonical Telugu text and its communicative intent remain unchanged, while meanings, explanations, pronunciation guidance, and transliteration may vary with the selected instruction language and its writing system.

## 2. Unit model

A sentence unit represents one complete concrete utterance that can be understood, spoken, read, written, or used in interaction. A unit must:

- have a stable identifier that does not depend on a course, chapter, or lesson number;
- be directly retrievable using that identifier;
- describe one coherent utterance and communicative intent;
- be reusable from multiple cards and lessons without duplicating its canonical definition; and
- contain no learner-specific or chapter-specific progression state.

A sentence unit may be treated as atomic for a particular learning purpose or exposed as a composite. A composite sentence references ordered vocabulary, grammar, character, or other sentence units and records the relationship among them rather than duplicating their canonical definitions. The sentence retains its own identity even when all components are independently accessible.

When a sentence unit is independently presented, the platform uses a Card that references the unit. **Sentence Card** is descriptive shorthand, not a Card subtype or inheritance relationship. The sentence unit remains the canonical content identity; the Card owns presentation properties and explicitly granted technical abilities.

The storage format and access mechanism are not yet decided. A unit may later be represented as an individual file, structured data record, content-management object, or application resource, provided its stable identifier remains resolvable.

## 3. Provisional identity scheme

Until the sentence model is finalised, proposed identifiers use these prefixes:

- `SENT-UTT-*` for standalone utterances;
- `SENT-RESP-*` for conventional response utterances; and
- `SENT-COMP-*` for composite or multi-part sentence forms that remain one learning object.

Identifiers are provisional until the sentence taxonomy is validated. Course, chapter, lesson, dialogue, and card definitions should reference the identifiers consistently once assigned.

## 4. Unit properties to determine

The exact property set is intentionally undecided. Product and curriculum design must determine whether a sentence unit needs properties such as:

- canonical Telugu text and punctuation;
- communicative intent;
- instruction-language-specific natural meaning, explanation, pronunciation approximation, and transliteration;
- natural and slow audio plus speaker or voice context;
- ordered vocabulary-unit, grammar-unit, character-unit, or sentence-unit references;
- mapping between referenced components and spans or functions in the concrete utterance;
- whether the unit is atomic for presentation or exposes a composite decomposition;
- register, politeness, speaker relationship, social context, dialect, and usage constraints;
- accepted contextual or spoken variants and the limits of equivalence;
- expected preceding or following sentence-unit relationships for dialogue;
- authored scene, image, illustration, or other media references;
- reading, speaking, listening, construction, and writing affordances;
- accessibility metadata;
- language-review status; and
- version.

These are candidates, not approved storage fields.

## 5. Composition and referencing requirements

- A card, dialogue, chapter, or lesson references a sentence unit by stable identifier.
- A Card presenting a sentence references its sentence unit rather than copying the unit definition.
- A sentence may compose vocabulary, grammar, character, or other sentence units by stable reference.
- Composition order must be explicit where it contributes to the utterance, while the model must not assume that instruction-language word order maps directly to Telugu.
- The referring lesson owns whether the sentence is introduced, recognised, imitated, adapted, created, reviewed, or assessed.
- The referring card owns its reveal order, interaction, media arrangement, prompt level, and evidence request.
- A sentence unit must not contain backlinks or progression state for a particular card, lesson, or chapter.
- A dialogue references sentence units and owns turn order and conversational relationships; it does not duplicate the sentence definitions.
- Updating a sentence unit must not silently change the intended learning outcome of a card or lesson that references an earlier approved version.

## 6. Open decisions

- What boundary separates a fixed-expression vocabulary unit from a sentence unit?
- When should a spoken utterance variant receive its own sentence identity?
- Should questions, answers, and dialogue turns use one sentence taxonomy or distinct subtypes?
- Which component mappings are required for word building, grammar highlighting, pronunciation support, and assessment?
- How should versioning protect dialogues, cards, and lessons when a sentence unit changes?
- Which identifiers are suitable for long-term content and application interfaces?
