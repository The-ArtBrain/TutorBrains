# Telugu Grammar Unit Specification

**Status:** Draft  
**Scope:** Independently accessible Telugu grammar and usage learning units

## 1. Purpose

This specification defines the shared model for Telugu grammar and usage units that can be referenced from any lesson in any chapter.

This document does not assign units to chapters or lessons. Each chapter owns its links, teaching relationship, examples, activities, and evidence requirements.

Grammar units must support any product instruction language. Canonical Telugu patterns and structural relationships remain unchanged, while names, explanations, meanings, contrasts, examples, terminology, and transliteration may have instruction-language-specific variants. English is the default instruction language, not part of a unit's canonical identity.

## 2. Unit model

Each grammar, sentence-pattern, or usage concept is an independently accessible unit. A unit must:

- have a stable identifier that does not depend on a chapter number;
- be directly retrievable using that identifier;
- describe one coherent learning object;
- be reusable from multiple lessons without duplicating its canonical definition; and
- contain no chapter-specific progression state.

Grammar units can and will be atomic or composite. A composite grammar unit is independently accessible under its own stable identifier and is defined by references to its component grammar units plus the relationship that combines them. Lessons may refer to the composite as one communicative pattern while other lessons address one of its components independently.

When a grammar unit is independently presented, the platform uses a Card that references the unit. **Grammar Card** is descriptive shorthand, not a Card subtype or inheritance relationship. The grammar unit remains the canonical content identity; the Card owns presentation properties and explicitly granted technical abilities.

The storage format and access mechanism are not yet decided. A unit may later be represented as an individual file, structured data record, content-management object, or application resource, provided its stable identifier remains resolvable.

## 3. Grammar presentation through Cards

A Card presenting a Grammar unit uses the flat Card contract in `platform_spec.md`. It does not inherit from a Grammar Card class, contain other Cards, or receive abilities merely because it references a Grammar unit.

The Card must reference one primary Grammar unit. It may reference additional Grammar, Sentence, Vocabulary, or Character units when they provide an example, contrast, decomposition, usage context, or assessment target. Those references do not copy the unit definitions into the Card.

### Grammar-related Card properties

Depending on its purpose, a Card may provide properties for:

- noticing, explanation, comparison, construction, comprehension, adaptation, production, review, assessment, or navigation purpose;
- the primary Grammar-unit reference and any related-unit references;
- canonical Telugu pattern, concrete examples, contrasts, or common-error references;
- localized concept name, meaning, explanation, terminology, and transliteration;
- communicative purpose, register, speaker relationship, dialect, and social context;
- natural or teaching-speed audio references;
- interaction, reveal, retry, accepted-variation, assessment-request, feedback-intent, and evidence policies;
- required and optional service-handle contracts plus the expected content, rubric, or options passed through them;
- submission-history scope for the Grammar unit; and
- accessibility semantics and alternatives.

These are Card properties, not additional Grammar-unit identity. The same Grammar unit may be presented by different Cards for explanation, recognition, sentence construction, dialogue use, review, or assessment.

### Grammar-related technical abilities

A Card may be explicitly granted the technical abilities needed for its purpose, including:

- **Present text** for Telugu patterns, examples, contrasts, and localized explanations;
- **Present transliteration** for instruction-language-specific support;
- **Speak or play audio** for example sentences, dialogue turns, rhythm, or intonation;
- **Listen** for spoken production;
- **Accept submission** for speech, text, choice, ordering, construction, or other configured responses;
- **Assess submission** for meaning, form, contextual appropriateness, or accepted variation;
- **Score submission** only when a valid scoring scale has been defined and a compatible registered evaluation service can provide a reliable result;
- **Reveal help** for progressive meaning, pattern, ending, contrast, or example guidance;
- **Record submission history** and **Retain raw evidence** under their separate policies;
- **Present submission history** for authorized review of earlier attempts; and
- **Navigate** to a Grammar unit, Sentence unit, Lesson, Chapter, or other stable target.

No bundle is automatic. For example, an explanation Card may present a grammar pattern without listening or assessing; a production Card receives only the submission and assessment abilities its activity requires.

## 4. Provisional identity scheme

Until the content model is finalised, proposed identifiers use these prefixes:

- `GRAM-USAGE-*` for politeness, register, and social usage;
- `GRAM-PATTERN-*` for sentence and dialogue patterns;
- `GRAM-PRON-*` for pronouns;
- `GRAM-VERB-*` for verb forms and agreement; and
- `GRAM-SOUND-*` for meaningful rhythm or intonation patterns.

Identifiers are provisional until the unit taxonomy is validated. Chapter and lesson documents should use the identifiers consistently once assigned.

## 5. Unit properties to determine

The exact property set is intentionally undecided. Product and curriculum design must determine whether a grammar unit needs properties such as:

- plain-language concept name localized to the selected instruction language;
- grammar or usage category;
- communicative purpose;
- canonical Telugu pattern;
- learner-facing explanation;
- instruction-language-specific meaning, explanation, terminology, and transliteration variants;
- prerequisites and related concepts;
- whether the unit is atomic or composite and, for a composite, its ordered component references;
- register, social context, and dialect constraints;
- contrastive examples and common mistakes;
- media or interaction assets;
- assessment affordances;
- language-review status; and
- version.

These are candidates, not approved requirements.

## 6. Grammar Card collections and Chapters

Grammar Cards are arranged by external ordered Card collections; a Card never contains another Card.

- A **Grammar** Chapter may consist directly of an ordered collection of Cards referencing Grammar units.
- A Chapter may group Cards by usage, pattern, pronoun, verb form, agreement, rhythm, intonation, communicative purpose, or another curriculum relationship without introducing Card subtypes.
- A Chapter may contain only Grammar-related Cards, may mix them with Sentence or Vocabulary-related Cards, and may include Lesson Cards.
- A Lesson Card references the Grammar units needed for its objective. The same unit may be reused by several Lesson Cards or other Cards without copying its definition.
- A composite Grammar unit references its component Grammar units. A Card presenting that composite may reference component units and concrete Sentence units, but it does not contain component Cards.
- The collection owns order, grouping, navigation, and curriculum placement. Each Card retains its own properties and explicit technical abilities.

## 7. Referencing requirements

- A Chapter Card or Lesson Card references a unit by stable identifier.
- A Card presenting grammar references its grammar unit rather than copying the unit definition.
- The referring Lesson Card owns the relationship to that unit, such as noticing, introduction, practice, reinforcement, or assessment.
- The referring Card owns its objectives, contextual examples, explanation depth, interaction, service-handle requirements, expected evaluation inputs, feedback intent, prompt level, retry behaviour, and Accomplishment rule. Registered services provide evaluation, speech, or feedback through handles bound during Card initialization.
- A unit must not contain backlinks or progression state for a particular chapter.
- Multiple lessons may reference the same unit independently.
- Composite units reference their components by stable identifier rather than duplicating the component definitions.
- Updating a unit must not silently change the intended learning outcome of a lesson that references it.

## 8. Grammar submission history

When a Grammar-related Card records a learner attempt, the durable Submission record must link to:

- the learner and authorized tutor context where applicable;
- the Card identity and version;
- the primary Grammar unit and any assessed Sentence, Vocabulary, Character, or related Grammar units;
- the Course, Chapter, Lesson, and Card-collection context;
- the submission mechanism, such as speech, text, choice, or construction;
- the assessment result or valid score, including **Not assessed** when applicable; and
- any separately retained raw recording or other evidence.

An authorized learner or tutor must be able to review all permitted submissions for one Grammar unit across Cards, Lessons, Chapters, and sessions. Deleting or expiring raw evidence need not delete an allowed nonsensitive attempt or progress record, but the product must make that distinction clear.

## 9. Open decisions

- What is the smallest useful atomic grammar unit: a form, a contrast, a productive pattern, a usage rule, or another learning object?
- Should every unit be stored separately, or can a structured collection still provide independent access?
- Which properties are required for every unit, and which depend on unit type?
- How should versioning protect existing lessons when a unit changes?
- How should prerequisites, related concepts, variants, and exceptions be represented?
- Which composition relationships and ordering rules are required for composite grammar units?
- Which identifiers are suitable for long-term application and content interfaces?
- Which unit properties are language-independent, and how are instruction-language-specific meaning, transliteration, and explanation variants attached?
- Which Grammar-related Card properties and technical abilities are required for the first release?
- Which Grammar Card collections should be represented directly as Chapters, and which benefit from Lesson grouping?
