# Telugu Tutor — Student Onboarding Guide

**Status:** Draft  
**Scope:** Student actions from first opening Telugu Tutor until the hand-off to Chapter 01  
**Primary learner:** Adult beginner in the first-pupil pilot  
**Capability source:** [Telugu Tutor Capability Matrix](capability_matrix.md)

## 1. Purpose and boundary

Onboarding prepares a student to begin learning without testing Telugu knowledge or collecting lesson evidence. It is a set of independent setup facts and explanations, not a workflow with its own orchestration, progress, or completion state. Each choice is retained when made; when a choice is absent, the applicable declared default is used.

The pre-chapter boundary ends when the student selects **Start Chapter 01**. The Chapter 01 welcome and setup activity begins after that selection.

Before Chapter 01, the student has:

- a usable guest or persistent learning identity;
- the correct student profile selected;
- an instruction language selected or its English default applied;
- access to Chapter 01 confirmed;
- the available accessibility, audio, speech, and writing alternatives explained; and
- the difference between ordinary progress data and optional sensitive evidence explained.

The product presents one decision at a time and uses the selected instruction language as soon as it is known. It does not require a permanent account, placement test, age, microphone access, camera access, writing sample, or blanket consent to retain future recordings or images.

The student profile is extensible, but extensibility is not permission to collect information speculatively. The current adult pilot records only information required by an active capability. It does not need the student's age.

## 2. Student actions before Chapter 01

| Step | What the student sees | What the student does | Result | Linked capabilities |
|---:|---|---|---|---|
| 1 | A short welcome and a language selector whose choices are identifiable in their own languages | Selects a supported instruction language or uses the clearly labelled English default | Onboarding, interface text, explanations, and transliteration use the resolved language; any fallback is disclosed. The preference is retained when selected | [Select instruction language `cap-LNG-0001`](capability_matrix.md#1-instruction-language-and-localization), [Apply default instruction language `cap-LNG-0002`](capability_matrix.md#1-instruction-language-and-localization), [Remember language preference `cap-LNG-0004`](capability_matrix.md#1-instruction-language-and-localization), [Localize onboarding `cap-LNG-0006`](capability_matrix.md#1-instruction-language-and-localization), [Disclose fallback language `cap-LNG-0017`](capability_matrix.md#1-instruction-language-and-localization), [Present adapted transliteration `cap-TRL-0001`](capability_matrix.md#2-transliteration) |
| 2 | A choice to continue as a guest, create an account, or sign in | Chooses one identity path; a returning student signs in, while a new student may remain a guest | A current learning identity exists without requiring account creation | [Use guest learning identity `cap-AUT-0001`](capability_matrix.md#16-identity-and-ability-based-authorization), [Create account `cap-AUT-0002`](capability_matrix.md#16-identity-and-ability-based-authorization), [Sign in `cap-AUT-0003`](capability_matrix.md#16-identity-and-ability-based-authorization) |
| 3 | A student-profile choice when the identity contains more than one profile | Selects the intended profile or creates a minimal profile when one does not exist | Progress and evidence belong to the intended student. Additional declared attributes can be added later, but age and other unused information are not requested now | [Maintain learner profiles `cap-AUT-0009`](capability_matrix.md#16-identity-and-ability-based-authorization), [Transfer guest progress `cap-AUT-0010`](capability_matrix.md#16-identity-and-ability-based-authorization), [Build extensible student profile `cap-AUT-0027`](capability_matrix.md#16-identity-and-ability-based-authorization) |
| 4 | The practical course outcome, **recognise -> imitate -> adapt -> create** approach, course structure, table of contents, learning modes, and supportive return after interruptions | Reviews how the course works and browses what it contains | The student understands the learning approach and how courses, chapters, lessons, and reusable units fit together | [Present course approach and contents `cap-CRS-0001`](capability_matrix.md#23-course-orientation-and-structure), [Greet student warmly `cap-COM-0001`](capability_matrix.md#4-tutor-communication-and-conduct), [Give concise instruction `cap-COM-0002`](capability_matrix.md#4-tutor-communication-and-conduct) |
| 5 | A Chapter 01 card describing the practical outcome: greet an elder, teacher, or unfamiliar adult in Telugu | Reviews the outcome and chooses Chapter 01 | The student knows what they will be able to do, rather than only what content they will view | [Present content catalogue `cap-BUY-0001`](capability_matrix.md#19-catalogue-purchase-and-subscription), [Present lesson mission `cap-LES-0001`](capability_matrix.md#3-lesson-and-session-orchestration) |
| 6 | Chapter access and readiness status | Continues if access is available; otherwise reviews the reason and valid access route. If earlier learning is recommended later, reviews that recommendation separately from ownership | Chapter 01 access is authorized without treating purchase as proof of educational readiness | [Check content entitlement `cap-ENT-0007`](capability_matrix.md#17-content-entitlement-and-educational-eligibility), [Explain locked content `cap-ENT-0008`](capability_matrix.md#17-content-entitlement-and-educational-eligibility), [Check educational prerequisite `cap-ENT-0011`](capability_matrix.md#17-content-entitlement-and-educational-eligibility), [Explain readiness recommendation `cap-ENT-0012`](capability_matrix.md#17-content-entitlement-and-educational-eligibility), [Authorize content use `cap-ENT-0013`](capability_matrix.md#17-content-entitlement-and-educational-eligibility) |
| 7 | A brief accessibility and participation-options summary | Uses supported defaults or selects relevant alternatives: keyboard operation, screen-reader labels, non-drag interactions, text alternatives to audio, and upload/camera/direct-writing routes | Selected preferences are retained in the extensible profile when needed. An absent preference uses accessible defaults and does not block learning | [Build extensible student profile `cap-AUT-0027`](capability_matrix.md#16-identity-and-ability-based-authorization), [Provide keyboard operation `cap-PRV-0009`](capability_matrix.md#14-consent-privacy-and-accessibility), [Provide screen-reader semantics `cap-PRV-0010`](capability_matrix.md#14-consent-privacy-and-accessibility), [Provide non-drag alternative `cap-PRV-0012`](capability_matrix.md#14-consent-privacy-and-accessibility), [Provide accessible writing route `cap-PRV-0013`](capability_matrix.md#14-consent-privacy-and-accessibility), [Provide audio text alternative `cap-AUD-0012`](capability_matrix.md#6-audio-presentation) |
| 8 | A plain-language privacy summary separating progress from sensitive evidence | Reviews what ordinary progress is saved, why recordings or writing may be requested later, and how retained evidence can be listed or deleted. The student does **not** give blanket evidence consent here | Each sensitive item still requires an explicit, in-context storage decision | [Explain evidence use `cap-PRV-0001`](capability_matrix.md#14-consent-privacy-and-accessibility), [Request evidence consent `cap-PRV-0002`](capability_matrix.md#14-consent-privacy-and-accessibility), [List saved evidence `cap-PRV-0004`](capability_matrix.md#14-consent-privacy-and-accessibility), [Delete sensitive evidence `cap-PRV-0005`](capability_matrix.md#14-consent-privacy-and-accessibility), [Minimize collected data `cap-PRV-0008`](capability_matrix.md#14-consent-privacy-and-accessibility) |
| 9 | A summary showing instruction language, identity/profile, Chapter 01 access, and links to course, accessibility, and privacy information | Corrects any setting if needed, then selects **Start Chapter 01** | The Chapter 01 welcome begins with no learning objective marked complete; full or fallback mode has not yet been chosen | [Change instruction language `cap-LNG-0003`](capability_matrix.md#1-instruction-language-and-localization), [Inspect granted abilities `cap-AUT-0020`](capability_matrix.md#16-identity-and-ability-based-authorization), [Evaluate ability authorization `cap-AUT-0021`](capability_matrix.md#16-identity-and-ability-based-authorization) |

## 3. Conditional cases

These cases appear only when relevant. They are not mandatory for every student.

### Account or guest

- A student may start as a guest. Registration is optional before Chapter 01.
- A returning student signs in and selects the correct student profile.
- If a guest later creates an account, guest progress can be transferred rather than discarded.
- Account recovery, export, deletion, and session management remain available account-management actions, not pre-chapter gates.

### Future profile information

- The first-pupil prototype does not ask for age because no current capability needs it.
- A future capability may require an additional profile attribute. It is added only when its purpose, use, and applicable privacy rules are defined.
- If child-specific content or participation is introduced later, guardian and child-safety capabilities can be applied then. Their existence in the catalogue does not justify collecting age now.

### Content access

- The current documents do not decide whether Chapter 01 is free, assigned, pilot-only, previewable, or paid. The product displays the configured status rather than assuming one.
- If access is locked, the student sees why and how it can legitimately be obtained.
- Purchase, subscription, invitation, and sponsored-access paths are conditional. If a purchase is offered, the student reviews the content, included abilities, price, duration, and charge before confirming it: [Present offer `cap-BUY-0002`](capability_matrix.md#19-catalogue-purchase-and-subscription), [Review purchase `cap-BUY-0007`](capability_matrix.md#19-catalogue-purchase-and-subscription), and [Complete purchase `cap-BUY-0008`](capability_matrix.md#19-catalogue-purchase-and-subscription).

### Missing localization

- If the selected instruction language is not fully supported, the product states which fallback language will appear.
- The student may accept the disclosed fallback or choose another supported instruction language.
- The product must not silently revert to English, and the Telugu learning objective remains unchanged.

## 4. What happens only after Chapter 01 starts

The following actions belong to the Chapter 01 **Welcome and setup** or later lesson activities, not the pre-chapter set:

1. The student chooses the normal 30-minute route or the five-minute fallback: [Start full lesson `cap-LES-0002`](capability_matrix.md#3-lesson-and-session-orchestration) and [Start fallback lesson `cap-LES-0003`](capability_matrix.md#3-lesson-and-session-orchestration).
2. The student completes the short replayable audio check: [Check audio readiness `cap-AUD-0010`](capability_matrix.md#6-audio-presentation).
3. Before the first recording, the student allows microphone access or selects **Continue without recording**: [Request microphone access `cap-SPC-0001`](capability_matrix.md#7-speech-collection-and-understanding) and [Skip recording `cap-SPC-0009`](capability_matrix.md#7-speech-collection-and-understanding).
4. During handwriting, the student chooses image upload, camera capture, or direct writing. Camera permission is requested only if camera capture is selected: [Request camera access `cap-INP-0001`](capability_matrix.md#8-image-camera-and-direct-writing) and [Switch writing method `cap-INP-0017`](capability_matrix.md#8-image-camera-and-direct-writing).
5. Before any recording, photograph, image, or stroke data is retained, the student receives the specific purpose and makes an explicit consent decision: [Request evidence consent `cap-PRV-0002`](capability_matrix.md#14-consent-privacy-and-accessibility) and [Record consent decision `cap-PRV-0003`](capability_matrix.md#14-consent-privacy-and-accessibility).

Moving these requests into the pre-chapter set would ask for permissions or consent before the student understands the immediate purpose. Denying microphone, camera, or evidence storage must not prevent lesson continuation.

## 5. Facts required before Chapter 01

There is no combined onboarding-complete record. The student can select **Start Chapter 01** when the independent facts required by Chapter 01 are available:

- an instruction language is selected, or the English default is applied;
- a guest or persistent identity and the intended student profile are active;
- Chapter 01 access is currently authorized; and
- any localization fallback is disclosed.

Course, accessibility, and privacy information remain reviewable. A saved preference is reused until the student changes it; an absent optional preference uses the declared accessible default. These setup facts must not create Chapter 01 learning evidence, objective statuses, or lesson completion. The first learning state remains **Not started** until the student starts Chapter 01.

## 6. Capability coverage

The capability catalogue explicitly covers the two outcomes that were previously implicit:

- [Present course approach and contents `cap-CRS-0001`](capability_matrix.md#23-course-orientation-and-structure) supplies the course approach, structure, and table of contents without assessing the student.
- [Build extensible student profile `cap-AUT-0027`](capability_matrix.md#16-identity-and-ability-based-authorization) retains only the profile information current capabilities need and allows declared attributes to be added later.

No onboarding-orchestration capability is required. Identity, profile, instruction language, accessibility preferences, content access, and consent remain independently governed capabilities and facts.
