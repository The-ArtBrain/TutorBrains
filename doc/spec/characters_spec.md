# Telugu Character Unit Specification

**Status:** Draft  
**Scope:** Independently accessible Telugu script learning units

## 1. Purpose

This specification defines the shared model for Telugu character and writing-system units that can be referenced from any lesson in any chapter.

This document does not assign units to chapters or lessons. Each chapter owns its links, teaching relationship, examples, activities, and evidence requirements.

Character units must support any product instruction language. Canonical Telugu forms remain unchanged, while accessible names, explanations, sound approximations, and transliteration may vary with the selected instruction language and its writing system. English and Roman-script values are defaults, not canonical substitutes for localized values.

## 2. Unit model

Each character, sign, mark, or combined form is an independently accessible unit. A unit must:

- have a stable identifier that does not depend on a chapter number;
- be directly retrievable using that identifier;
- describe one coherent learning object;
- be reusable from multiple lessons without duplicating its canonical definition; and
- contain no chapter-specific progression state.

Character units can and will be atomic or composite. A composite character unit is independently accessible under its own stable identifier and is defined by references to its component units plus the relationship that combines them. A composite is not merely an inline copy of its components; lessons may refer to the composite as one teachable or assessable object while still traversing its component links.

When a character unit is independently presented, the platform uses a Card that references the unit. **Character Card** is descriptive shorthand, not a Card subtype or inheritance relationship. The character unit remains the canonical content identity; the Card owns presentation properties and explicitly granted technical abilities.

The storage format and access mechanism are not yet decided. A unit may later be represented as an individual file, structured data record, content-management object, or application resource, provided its stable identifier remains resolvable.

## 3. Character presentation through Cards

A Card presenting a Character unit uses the flat Card contract in `platform_spec.md`. It does not inherit from a Character Card class, contain other Cards, or receive abilities merely because it references a Character unit.

The Card must reference one primary Character unit. It may reference additional Character, Vocabulary, Sentence, or Grammar units when they provide an example, contrast, decomposition, or assessment target. Those references do not copy the unit definitions into the Card.

### Character-related Card properties

Depending on its purpose, a Card may provide properties for:

- orientation, recognition, pronunciation, reading, construction, handwriting, review, assessment, or navigation purpose;
- the primary Character-unit reference and any related-unit references;
- canonical Telugu display and the exact form or feature to emphasize;
- localized name, explanation, pronunciation approximation, and transliteration;
- natural or teaching-speed audio references;
- writing model, proportions, stroke guidance, or comparison reference;
- authored example imagery or learner-submission presentation;
- interaction, reveal, retry, assessment-request, feedback-intent, and evidence policies;
- required and optional service-handle contracts plus the expected content or criteria passed through them;
- submission-history scope for the Character unit; and
- accessibility semantics and alternatives.

These are Card properties, not additional Character-unit identity. The same Character unit may be presented by different Cards for recognition, pronunciation, handwriting, review, or assessment.

### Character-related technical abilities

A Card may be explicitly granted the technical abilities needed for its purpose, including:

- **Present text** for the Telugu form and localized guidance;
- **Present transliteration** for instruction-language-specific pronunciation support;
- **Speak or play audio** for a sound, syllable, character name, or example;
- **Listen** and **Accept submission** for learner pronunciation;
- **Present authored media** for reviewed writing or shape guidance;
- **Accept learner image**, **Capture camera input**, or **Accept direct writing** for handwriting evidence;
- **Assess submission** for reliable recognition, pronunciation, or handwriting feedback;
- **Score submission** only when a valid scoring scale has been defined and a compatible registered evaluation service can provide a reliable result;
- **Reveal help** for progressive sound, form, component, or example guidance;
- **Record submission history** and **Retain raw evidence** under their separate policies;
- **Present submission history** for authorized review of earlier attempts; and
- **Navigate** to a Character unit, Lesson, Chapter, or other stable target.

No bundle is automatic. For example, a reference Card may present a character without being able to listen, write, assess, or score; a handwriting Card receives only the abilities its activity requires.

## 4. Provisional identity scheme

Until the content model is finalised, proposed identifiers use these prefixes:

- `CHAR-C-*` for consonants;
- `CHAR-V-*` for independent vowels;
- `CHAR-S-*` for dependent vowel signs and other marks; and
- `CHAR-F-*` for combined or conjunct forms.

Identifiers are provisional until the unit taxonomy is validated. Chapter and lesson documents should use the identifiers consistently once assigned.

## 5. Unit properties to determine

The exact property set is intentionally undecided. Product and curriculum design must determine whether a character unit needs properties such as:

- Telugu form and accessible name;
- character category;
- sound and pronunciation guidance;
- instruction-language-specific transliteration, pronunciation approximation, and explanation variants;
- writing function;
- component or combination relationships;
- whether the unit is atomic or composite and, for a composite, its ordered component references;
- prerequisites;
- recognition, reading, and handwriting variants;
- example words independent of any one lesson;
- media and rendering assets;
- accessibility metadata;
- dialect or pronunciation notes; and
- language-review status and version.

These are candidates, not approved requirements.

## 6. Character Card collections and Chapters

Character Cards are arranged by external ordered Card collections; a Card never contains another Card.

- An **Alphabet** or **Telugu script** Chapter may consist directly of an ordered collection of Cards referencing Character units.
- A Chapter may group Cards for vowels, consonants, vowel signs, marks, combined forms, recognition, pronunciation, or writing without introducing a Card subtype for any group.
- A Chapter may contain only Character-related Cards, may mix them with Vocabulary or Sentence-related Cards, and may include Lesson Cards.
- A Lesson Card references the Character units needed for its objective. The same unit may be reused by several Lesson Cards or other Cards without copying its definition.
- A composite Character unit references its component Character units. A Card presenting that composite may reference the component units for display or explanation, but it does not contain component Cards.
- The collection owns order, grouping, navigation, and curriculum placement. Each Card retains its own properties and explicit technical abilities.

## 7. Referencing requirements

- A Chapter Card or Lesson Card references a unit by stable identifier.
- A Card presenting a character references its character unit rather than copying the unit definition.
- The referring Lesson Card owns the relationship to that unit, such as orientation, introduction, practice, reinforcement, or assessment.
- The referring Card owns its objectives, contextual examples, interaction, service-handle requirements, expected evaluation inputs, feedback intent, prompt level, retry behaviour, and Accomplishment rule. Registered services provide evaluation, speech, or feedback through handles bound during Card initialization.
- A unit must not contain backlinks or progression state for a particular chapter.
- Multiple lessons may reference the same unit independently.
- Composite units reference their components by stable identifier rather than duplicating the component definitions.
- Updating a unit must not silently change the intended learning outcome of a lesson that references it.

## 8. Character submission history

When a Character-related Card records a learner attempt, the durable Submission record must link to:

- the learner and authorized tutor context where applicable;
- the Card identity and version;
- the primary Character unit and any assessed related units;
- the Course, Chapter, Lesson, and Card-collection context;
- the submission mechanism, such as speech, image, camera, or direct writing;
- the assessment result or valid score, including **Not assessed** when applicable; and
- any separately retained raw recording, image, or stroke evidence.

An authorized learner or tutor must be able to review all permitted submissions for one Character unit across Cards, Lessons, Chapters, and sessions. Deleting or expiring raw evidence need not delete an allowed nonsensitive attempt or progress record, but the product must make that distinction clear.

## 9. Open decisions

- What is the smallest useful atomic character unit: a Unicode character, a taught sound-form relationship, or another learning object?
- Should every unit be stored separately, or can a structured collection still provide independent access?
- Which properties are required for every unit, and which depend on unit type?
- How should versioning protect existing lessons when a unit changes?
- How should related units, prerequisites, variants, and combinations be represented?
- Which composition relationships and ordering rules are required for composite character units?
- Which identifiers are suitable for long-term application and content interfaces?
- Which unit properties are language-independent, and how are instruction-language-specific transliteration and explanation variants attached?
- Which Character-related Card properties and technical abilities are required for the first release?
- Which Character Card collections should be represented directly as Chapters, and which benefit from Lesson grouping?
