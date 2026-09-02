# Telugu Tutor — Common Product Specification

**Status:** Draft  
**Scope:** Requirements inherited by every chapter and lesson  
**Primary learner:** Adult beginner using a configurable instruction language; English is the default

## 1. Purpose

The product behaves like a patient Telugu tutor. Each activity Card listens to or receives the pupil's attempt, calls its bound evaluation handle with the expected and submitted content, and may call a bound feedback handle with the returned Evaluation. The pupil chooses which accessible Card to open and when to leave or return.

This is not a deck of vocabulary cards or a fixed slideshow. The pupil should feel that a tutor is present, paying attention, and adjusting the lesson to their response.

Each chapter specification defines its own learning outcome, content, activities, evidence, timings, and completion criteria. If a chapter requirement conflicts with this document, the explicit chapter requirement takes precedence and the exception should be documented.

Every chapter must link its active script items to `characters_spec.md`, active vocabulary to `vocabulary_spec.md`, active concrete utterances to `sentence_spec.md`, and active grammar or usage concepts to `grammar_spec.md`. A referenced unit that merely appears in lesson content should not automatically become a learning objective.

### Instruction language and transliteration

The language used for instructions, explanations, meanings, feedback, onboarding, and interface text is the **instruction language**. It can be any supported language. English is the default when the pupil has not selected another language; English is not a permanent product or curriculum constraint.

The pupil must be able to select and later change the instruction language without losing lesson progress. Telugu remains the target language and should progressively occupy more of the learning activity regardless of the selected instruction language.

Transliteration is instruction-language dependent. It must use a script, spelling convention, and pronunciation guidance suitable for a reader of the selected instruction language. Changing the instruction language may therefore change both the transliteration script and the approximation itself; the product must not assume that Roman-script transliteration is universal.

Content must keep these values separate:

- canonical Telugu text;
- meaning in the selected instruction language;
- transliteration configured for the selected instruction language and script; and
- language-independent learning and progress evidence.

Changing the instruction language must not change the canonical Telugu, the chapter objective, or previously earned progress. When localized meaning or transliteration is unavailable, the tutor must disclose the fallback language rather than silently showing English.

## 2. Common product goals

- Turn each lesson plan into a guided one-to-one tutoring experience.
- Make the pupil use Telugu early in the session.
- Move through the course loop: **recognise -> imitate -> adapt -> create**.
- Use Telugu audio before explanation, meaning, or transliteration in the selected instruction language.
- Give feedback that is specific, brief, and focused on the highest-value improvement.
- Adapt help to the pupil's demonstrated need rather than showing all help at once.
- Capture learning evidence that can validate and improve the course.
- Make returning to the locally recorded last-accessed Card easy and free of guilt without restricting access to other Cards.

## 3. Tutor principles

### The tutor leads, then gets out of the way

Every activity begins with a clear spoken instruction or model. As the pupil succeeds, the tutor removes meaning, transliteration, word construction, and model audio in that order.

### One turn, one task

The open Card presents no more than one required question or action at a time. Supporting material may be revealed on demand. A Card may represent a Lesson or an activity; that boundary is still evolving and does not require a universal activity sequence. The pupil may leave an open Card and return later.

### Audio comes first

The pupil hears an expression before seeing its meaning in the selected instruction language. Telugu script remains visible once introduced. Instruction-language-appropriate transliteration is temporary help, not the primary representation.

### Communication before correction

The tutor first decides whether the intended message was understandable and appropriate. It then offers at most one pronunciation improvement and one language correction before inviting another attempt.

### Evidence before celebration

Praise names what the pupil actually did, such as completing a response without an instruction-language meaning or making a question ending clearer. Generic celebration should be occasional and secondary.

### Return without punishment

Card access, student content, Evaluations, Submissions, and Accomplishments are recorded as applicable. A returning pupil may reopen the last-accessed Card or choose any other accessible Card; missed time is never described as failure.

## 4. Tutor contract

The tutor must:

- greet the pupil warmly and state the practical mission;
- speak in short, direct sentences;
- demonstrate Telugu naturally before explaining it;
- ask the pupil to predict meaning from tone and context when appropriate;
- wait for a response instead of immediately revealing the answer;
- accept semantically equivalent answers during comprehension checks;
- distinguish silence, a technical recording problem, an understandable attempt, and an attempt needing help;
- provide help progressively;
- permit replay and **Show me** without penalising the pupil;
- explain the usage and social context of the target language;
- never invent a score when speech, handwriting, or another response cannot be evaluated reliably;
- provide an accessible alternative when a microphone, camera, or assessment capability is unavailable; and
- close with an independent performance and a concise learning summary.

The tutor must not:

- lecture through reference material that is not part of the active lesson;
- expose internal confidence scores or technical recognition output;
- interrupt a pupil while they are speaking;
- correct every difference from the model;
- say **Wrong** when an attempt is understandable but imperfect;
- force repeated attempts after two unsuccessful tries at the same turn;
- use red failure states or shame-based return messages; or
- let a general chat response replace the chapter's learning objective.

## 5. Adaptive tutoring

### Help ladder

When the pupil is stuck, reveal only the applicable steps, in this order:

1. replay the natural model;
2. replay a slower model;
3. show the Telugu expression;
4. highlight the relevant sound, syllable, character, or ending;
5. show the natural meaning in the selected instruction language;
6. show transliteration configured for the selected instruction language and script; and
7. let the pupil hear and echo the complete answer.

Stop revealing help as soon as the pupil can complete the current Card. Do not force every help step.

### Response rules

| Observed response | Tutor behaviour |
|---|---|
| Understandable and appropriate | Record the Card Evaluation and applicable Accomplishment, then confirm specifically |
| Understandable with a useful improvement | Confirm meaning, give one improvement, and allow one retry |
| Different but valid answer | Accept it and model the chapter expression |
| No response | Wait, then offer replay or a smaller prompt |
| Two unsuccessful attempts | Model the answer, echo once, mark **Revisit**, and let the pupil retry later or leave the Card |
| Assessment confidence too low | Say the tutor could not assess the response; offer replay, retry, or self-check |
| Required device capability unavailable | Continue with an accessible alternative and mark the objective **Not assessed** when necessary |
| Pupil asks an off-topic question | Answer briefly if safe, then return to the open Card |

## 6. Common experience and interface requirements

A Card is a domain concept with a corresponding interface, not merely a visual container. It may represent a whole Lesson or an independently meaningful activity. The exact selection rule is not finalized. Cards remain flat under the current contract and may reference peer Cards through normal navigation rather than containing child Cards.

Curriculum authors may use the following labels as optional planning lenses:

| Optional label | Possible lesson activity                                                                                                                                                                      |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Listen** | Present the target Telugu audio or other primary input first and invite the pupil to notice, distinguish, or predict before explanation.                                                        |
| **Learn**  | Teach meaning, usage, form, rhythm, or pronunciation with progressive help and an active pupil response.                                                                                        |
| **Build**  | Let the pupil construct, arrange, distinguish, read, type, or write the lesson's language forms. Building may use characters, syllables, words, sentences, or another chapter-appropriate unit. |
| **Talk**   | Move from guided production to an understandable spoken or otherwise accessible communicative performance.                                                                                      |
| **Check**  | Run a short lesson-scoped check, record supported evidence, and summarise what the pupil demonstrated without blocking access to other Cards.                                                   |

These labels are not required Card identities, required phases, a prescribed order, or student-interface elements. A Lesson may use some, all, or none of them and may arrange its activities differently. If an activity needs independent addressing or reuse, it may become a separate peer Card based on that lesson's needs, not merely because it resembles one of these labels. A future Chapter test remains separate from the Lesson Card and requires its own specification.

Each open Card uses one stable layout:

- top: chapter and Lesson context with the current Lesson Card identified;
- centre: the current Telugu expression, scene, or task;
- below: contextual support such as meaning or word construction;
- bottom: one primary action and a small set of help controls; and
- persistent: pause, exit, and audio controls.

Do not expose **Listen**, **Learn**, **Build**, **Talk**, or **Check** merely to reveal internal lesson planning. When a Lesson links to another independent Card or destination, that navigation must be understandable without relying on colour alone. Use links or other navigation semantics when selecting a distinct resource; do not expose controls as tabs merely because they are arranged in one row.

Every speaking activity defines these visible states:

1. ready;
2. listening;
3. processing;
4. feedback available;
5. retry offered;
6. complete; and
7. assessment unavailable.

Processing must time out gracefully. The pupil must never lose a response or become trapped behind a spinner.

### Written input and handwriting

Writing is a core learning capability. When a lesson requires written input, the tutor must support these three mechanisms:

1. **Image upload:** choose an existing image of writing from the device.
2. **Camera capture:** photograph writing completed on paper or another physical surface.
3. **Direct on-screen writing:** write on a touch screen or drawing surface using a stylus or finger, or use a mouse or other pointing device.

The pupil chooses the available mechanism that works best for them. A chapter may recommend one mechanism for a particular activity, but it must not treat the physical input tool as part of language proficiency.

All three mechanisms must feed the same tutoring loop:

1. state exactly what the pupil should write;
2. collect the written sample;
3. show a preview before submission;
4. let the pupil clear, undo, retake, replace, or resubmit as appropriate;
5. confirm that the sample is visible and complete enough to assess;
6. identify recognisable writing before giving at most one high-value improvement;
7. request no more than one corrected sample before continuing; and
8. save accepted evidence only with consent and provide a delete action.

Direct writing must preserve the original strokes for replay or later analysis when the pupil consents. The drawing surface must support appropriate Telugu character proportions, clear/reset, undo, and submission without accidental page scrolling while writing. Pointer, touch, and stylus input must not require separate lesson content.

If the tutor cannot confidently assess a sample, it must say so and offer another input mechanism, a retry, or continuation with the objective marked **Not assessed**. It must never fabricate handwriting feedback. Failure of one input mechanism must not block the other mechanisms.

### Accessibility and language display

- Telugu text must be large enough to distinguish vowel signs and conjunct forms.
- Do not use colour alone to communicate correctness or the current dialogue turn.
- All controls require screen-reader labels and visible keyboard focus.
- Every interaction requires an accessible alternative to drag-and-drop.
- Writing controls must expose clear labels and instructions; when direct freehand input is not accessible, image upload, camera capture, or another equivalent evidence route must remain available.
- Model audio requires a text alternative after the initial listen-first activity.
- Slow audio should preserve natural pitch where feasible.
- Instructions use plain language in the selected instruction language and expand unfamiliar terminology on first use.

## 7. Progress, Accomplishments, and return

Every chapter supports these states:

- **Not started**
- **In progress**
- **Fallback completed**, when the chapter defines a fallback route
- **Lesson completed**
- **Ready to revisit**

Lesson and Chapter states are derived from their configured Card- and unit-scoped Accomplishments. A Lesson Card may include an exit check when required, but that activity does not imply a separate Card or gate access to other Cards. Completion does not require every objective to be independent unless the relevant curriculum specification explicitly requires it.

Per-objective evidence uses **Independent**, **Prompted**, **Revisit**, or **Not assessed**. Each chapter defines the objectives to which those statuses apply.

- Update the Student Card map after applicable access, help, submission, Evaluation, and Accomplishment events.
- Record the last-accessed Card locally on the current device.
- On return, offer the last-accessed Card and direct access to every other accessible Card.
- Cross-device recovery of the last-accessed Card is not required.
- Let the pupil restart a chapter without silently deleting earlier baseline evidence.
- Preserve completed fallback work when the pupil returns to the full lesson.

## 8. Data and privacy

Collect only what is required to evaluate learning and the tutor experience. Common evidence may include:

- usage mode, duration, Cards accessed, and derived completion state;
- selected instruction language and any language change during the session;
- help and prompt levels used for each objective;
- exit-check results and confidence before and after a session;
- pupil-reported difficulty, enjoyment, and confusing instructions;
- leave, return, fallback, retry, and last-access events; and
- recordings or images needed for learning evidence, only with explicit consent.

Do not use time spent as the main success measure. Do not store raw audio, photographs, direct-writing strokes, or other sensitive pupil submissions without explaining their use and providing a deletion action.

## 9. Common acceptance criteria

- Every Card represents a stated domain concept and has a corresponding presentation; whether a Lesson uses one Lesson-level Card or independently meaningful activity Cards remains an open design decision.
- A Lesson uses only the activities needed for its objective; **Listen**, **Learn**, **Build**, **Talk**, and **Check** are optional internal labels rather than required steps or student-interface elements.
- Leaving or revisiting a Lesson Card does not force a universal sequence or erase recorded work.
- The tutor presents no more than one required task at a time.
- English is the default instruction language, and another supported language can be selected or changed without losing progress.
- Instructions, meanings, explanations, prompts, feedback, interface text, and transliteration use the selected instruction-language variant.
- Transliteration is not required to use Roman script when another script or convention better serves the selected instruction language.
- Changing the instruction language does not change canonical Telugu content, objectives, evidence, or completion state.
- No Lesson Card consists only of passive reading when its objective requires an active learner response.
- Help controls are initially hidden where the chapter specifies and can be revealed independently.
- The tutor records the highest help level used for an objective.
- After two unsuccessful attempts, the Card models the configured answer, marks **Revisit**, and allows the pupil to retry later or leave.
- An unavailable or low-confidence assessment never produces fabricated feedback.
- A device or assessment failure never prevents the pupil from continuing.
- Refreshing or leaving a Card does not erase Student Card-map entries, Submissions, Evaluations, or Accomplishments already recorded.
- A returning pupil is offered the locally recorded last-accessed Card without losing direct access to other Cards.
- All Telugu text renders correctly on supported screen sizes.
- The lesson is operable by keyboard, and state is understandable without relying on colour.
- Audio controls, recording state, dialogue turns, and feedback have screen-reader-accessible labels.
- A writing activity supports image upload, camera capture, and direct on-screen writing with stylus, finger, or mouse.
- Written-input mechanisms produce equivalent objective status and feedback rules.
- The pupil can preview, correct, resubmit, and delete a written sample.

## 10. Common testing expectations

Observe a pupil completing each prototype without coaching outside the interface. Record:

1. where the pupil first hesitates;
2. whether help and response controls are understood;
3. whether feedback changes the next attempt;
4. when attention drops;
5. whether the independent performance is meaningfully independent; and
6. whether the completion summary matches what the pupil believes they learned.

Each chapter adds content-specific observations and follow-up questions. Before pupil testing, manually check every applicable acceptance criterion, Telugu content, supported screen size, permission-denial path, unavailable-assessment path, refresh and last-access return path, direct Card navigation, consent flow, and deletion control.
