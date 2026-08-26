# Chapter 1 Tutor — Product Requirements Document

**Status:** Draft for first-pupil prototype  
**Scope:** Chapter 1, Lesson 1 — Greet Someone  
**Primary learner:** Adult beginner using a configurable instruction language; English is the default  
**Target session:** 30 minutes, with a five-minute fallback  
**Source lesson:** [LESSON_01_GREETINGS.md](LESSON_01_GREETINGS.md)
**Pre-chapter onboarding:** [student_onboarding_guide.md](student_onboarding_guide.md)  
**Common requirements:** [common_spec.md](common_spec.md)  
**Character progression:** [characters_spec.md](characters_spec.md)  
**Grammar progression:** [grammar_spec.md](grammar_spec.md)

## 1. Relationship to the common specification

This chapter inherits the tutor behaviour, adaptive help, interface, accessibility, progress, privacy, and common acceptance requirements in `common_spec.md`. This document defines the Chapter 01 outcome, greeting content, lesson flow, evidence, and chapter-specific release criteria.

### Linked learning specifications

The identifiers below refer to independently accessible units governed by `characters_spec.md` and `grammar_spec.md`. Chapter 01 owns every relationship, contextual example, activity, and evidence requirement in these mappings.

#### Character-unit links

| Unit ID | Form or concept | Chapter 01 examples | Chapter 01 relationship |
|---|---|---|---|
| `CHAR-C-NA` | **న** (`na`) | **నమస్కారం, బాగున్నారా, బాగున్నాను** | Introduce, Practise, Assess |
| `CHAR-C-MA` | **మ** (`ma`) | **నమస్కారం, మీరు** | Introduce, Practise, Assess |
| `CHAR-C-SA` | **స** (`sa`) | **నమస్కారం** | Introduce, Practise |
| `CHAR-C-KA` | **క** (`ka`) | **నమస్కారం** | Introduce, Practise |
| `CHAR-C-RA` | **ర** (tapped or lightly rolled `ra`) | **నమస్కారం, బాగున్నారా, మీరు** | Introduce, Practise |
| `CHAR-C-BA` | **బ** (`ba`) | **బాగున్నారా, బాగున్నాను** | Introduce, Practise |
| `CHAR-C-GA` | **గ** (`ga`) | **బాగున్నారా, బాగున్నాను** | Introduce, Practise |
| `CHAR-S-AA` | **ా** changes inherent `a` to long `ā` | **కా, బా, నా, రా** | Introduce, Practise, Assess |
| `CHAR-S-II` | **ీ** changes the inherent vowel to long `ī` | **మీ** | Introduce, Practise |
| `CHAR-S-U` | **ు** changes the inherent vowel to `u` | **గు, ను, రు** | Introduce, Practise |
| `CHAR-S-VIRAMA` | **్** removes a consonant's inherent vowel | **స్, న్** | Introduce, Practise |
| `CHAR-S-ANUSVARA` | **ం** represents a context-dependent nasal sound | **రం** | Introduce, Practise |
| `CHAR-F-NNA` | doubled **న్న** | **బాగున్నారా, బాగున్నాను** | Introduce, Practise |

The complete Telugu character map is an orientation reference only. It is not an active recall, reading, or handwriting objective.

Chapter 01 character evidence requires the pupil to recognise **మ** and **న**, explain the long **ā** sign, connect active forms to the spoken dialogue, handwrite the active basic consonants and **నమస్కారం**, and act on one useful handwriting correction.

#### Grammar-unit links

| Unit ID | Chapter 01 concept or pattern | Chapter 01 relationship |
|---|---|---|
| `GRAM-USAGE-RESPECTFUL` | Respectful **నమస్కారం**, **బాగున్నారా?**, and **మీరు?** for an elder, teacher, or unfamiliar adult | Introduce, Practise, Assess |
| `GRAM-PATTERN-GREETING-EXCHANGE` | greet -> ask how someone is -> answer -> ask back | Introduce, Practise, Assess |
| `GRAM-PRON-MEERU` | Respectful **మీరు?** meaning “And you?” in this exchange | Introduce, Practise |
| `GRAM-VERB-WELL-QUESTION-RESPECTFUL` | **బాగున్నారా?** as the respectful question | Notice, Practise, Assess |
| `GRAM-VERB-WELL-FIRST-PERSON` | **బాగున్నాను** as the first-person answer | Notice, Practise, Assess |
| `GRAM-PATTERN-ASK-BACK` | **బాగున్నాను. మీరు?** as a short reciprocal question | Introduce, Practise, Assess |
| `GRAM-SOUND-QUESTION-INTONATION` | Slight rise at the end of **బాగున్నారా?** | Notice, Practise |

English meanings shown in this draft are default-language examples. In the product, meanings, explanations, prompts, feedback, and transliteration must use the pupil's selected instruction language. Transliteration may change its script and phonetic approximation when that language changes.

Chapter 01 teaches the question and answer initially as useful whole patterns rather than as a complete verb-conjugation table. Evidence requires the pupil to select respectful forms, distinguish the question from the answer, use **మీరు?** to ask back, and complete the exchange with limited or no prompting.

The chapter flow below defines how these linked items are taught and what Chapter 01 evidence is collected.

## 2. Chapter outcome

By the end of the session, the pupil should be able to:

1. say **నమస్కారం** as a respectful greeting;
2. ask **బాగున్నారా?** with understandable rhythm and question intonation;
3. respond with **బాగున్నాను. మీరు?**;
4. complete the greeting exchange with limited or no prompting;
5. recognise **మ** and **న** inside the target expressions;
6. explain that **ా** changes the vowel to a long **ā** sound; and
7. handwrite the active characters and a recognisable **నమస్కారం**, then improve the sample from tutor feedback.

Success means understandable communication, not a perfect accent or complete recall of the Telugu character system.

## 3. Chapter-specific product goals

- Make the pupil speak Telugu within the first three minutes.
- Guide the pupil from hearing the greeting to performing it independently.
- Capture evidence that validates the Chapter 01 lesson before later chapters are built.

## 4. Non-goals for the first prototype

- Teaching or testing the complete Telugu alphabet.
- Providing open-ended Telugu conversation outside the chapter's greeting scenario.
- Claiming precise accent grading or native-level pronunciation assessment.
- Supporting children and teenagers with the same presentation. Those versions require separate research and testing.
- Adding points, leaderboards, punitive streaks, social feeds, or elaborate game mechanics.
- Selecting the long-term application architecture, pricing model, or final artificial intelligence stack.

## 5. Chapter-specific application of tutor principles

- The independent greeting is the point at which the tutor fully gets out of the way.
- Telugu audio precedes meaning and instruction-language-appropriate transliteration during the first greeting listen.
- Praise and correction refer to observable features of the greeting, such as respectful usage, long vowels, doubled **న్న**, or question intonation.

## 6. Primary user story

As a beginner who cannot yet hold a Telugu conversation, I want a tutor to guide me through a real greeting, listen while I practise, and give me just enough help so that I can greet a Telugu speaker independently by the end of one session.

## 7. Chapter-specific tutor contract

In addition to the common tutor contract, the Chapter 01 tutor must:

- explain respectful usage for the greeting dialogue;
- allow the pupil to skip microphone activities and continue in listen-and-self-rate mode;
- keep the complete Telugu character map as optional orientation rather than required study; and
- close with one complete greeting performance and a concise summary of the demonstrated greeting skills.

## 8. Experience structure

Chapter 01 Lesson 1 implements the common five-Card Lesson contract. The rows below are five flat, directly navigable Cards, not sequential phases or Cards nested inside another Card.

| Card | Target time | Included Chapter 01 activities | Pupil action | Evidence captured |
|---|---:|---|---|---|
| **Listen** | 3 min | Welcome and setup; hear the complete exchange | Chooses the full or fallback route, checks audio, and infers situation, repetition, and question | Session choice, audio readiness, comprehension responses |
| **Learn** | 5 min | Understand and imitate the four expressions | Listens, notices meaning and respectful usage, repeats, and requests help when needed | Help used, attempt status |
| **Build** | 12 min | Script orientation; construct the greeting words; submit handwriting | Matches sounds and forms, assembles expressions, recognises active characters, and writes the required sample | Script comfort, recognition, construction, and writing results |
| **Talk** | 9 min | Guided conversation; independent performance | Completes both dialogue roles and performs one complete greeting | Prompt level per line, baseline recording, intelligibility status |
| **Check** | 1 min | Exit check and reflection | Recalls, identifies, performs, and reflects | Independent, Prompted, Revisit, or Not assessed |

The prototype may vary timings based on pupil responses, but should normally finish between 25 and 35 minutes.

The learner may open or revisit any accessible Lesson Card. The order above remains pedagogical guidance, not Lesson-controlled orchestration. The **Check** Card assesses this Lesson only; it is not the future Chapter test.

## 9. Detailed tutor flow

### 9.1 Welcome and setup — Listen Card

The first screen says what the pupil will be able to do, not what content they will consume:

> In this lesson, you will greet an elder, teacher, or unfamiliar adult in Telugu. By the end, you will perform the exchange yourself.

Required actions:

- **Start the 30-minute lesson**
- **I only have five minutes**

Before the first recording, request microphone access in context and provide **Continue without recording**. Include a short audio check with replay.

### 9.2 Hear the greeting first — Listen Card

Play the full exchange once without text. Then ask the three lesson questions one at a time:

1. Are they beginning or ending a conversation?
2. Which expression do you hear twice?
3. Which line sounds like a question?

After the pupil responds, replay the exchange with Telugu script. Meaning and instruction-language-appropriate transliteration remain hidden until requested or until the first failed comprehension attempt.

### 9.3 Understand and imitate — Learn Card

Teach one expression at a time:

| Expression | Tutor emphasis | Usage note |
|---|---|---|
| నమస్కారం | steady respectful greeting | Suitable for an unfamiliar adult, elder, or teacher |
| బాగున్నారా? | long vowels, doubled **న్న**, rising question ending | Respectful “How are you?” |
| బాగున్నాను | contrast final **ను** with question **రా** | “I am well” |
| మీరు? | long **మీ** | Respectful “And you?” |

For each expression:

1. play natural audio;
2. invite the pupil to repeat;
3. let the pupil replay or slow the model;
4. evaluate only for broad intelligibility in the prototype;
5. give one short piece of feedback; and
6. ask for one retry only when it is likely to help.

The pupil can tap **Meaning**, **Say it slowly**, or **Show transliteration**. These controls are recorded as scaffolding use, never as errors.

### 9.4 Script orientation — Build Card

Show the complete Telugu character map as an optional, scrollable reference so the writing system has visible structure. Clearly label it:

> A map for orientation — not a test today.

The guided path focuses only on **న, మ, స, క, ర, బ, గ** and the forms **ా, ీ, ు, ్, ం, న్న**. Do not require the pupil to scroll through or memorise the full map before continuing.

### 9.5 Build the greeting words — Build Card

Use interactive construction rather than a static explanation:

- play **నమస్కారం**, then ask the pupil to choose the matching written word;
- assemble **న + మ + స్ + కా + రం** in order;
- contrast **బాగున్నారా** and **బాగున్నాను** by highlighting their different endings;
- ask the pupil to locate **మ** and **న** inside familiar words;
- demonstrate **బ -> బా** and ask what changed;
- provide a handwriting prompt for **న, మ, స, క, ర, బ, గ** and one copy of **నమస్కారం**.

The required Chapter 01 writing sample is **న, మ, స, క, ర, బ, గ** written twice and **నమస్కారం** written once. The pupil submits it using any common written-input mechanism:

1. upload an existing image;
2. photograph writing completed on paper; or
3. write directly on screen using a stylus, finger, or mouse.

The handwriting interaction must:

1. offer all three input mechanisms before collection;
2. request camera permission only when the pupil chooses camera capture and explain why it is needed;
3. provide **Use**, **Retake** or **Clear**, **Undo** where applicable, and **Choose another method** actions;
4. show a preview before submission;
5. check first that the writing is visible and complete enough to review;
6. identify whether **న, మ, స, క, ర, బ, గ** and **నమస్కారం** are present;
7. show where a character is recognisable and where one high-value improvement would help;
8. ask for no more than one corrected sample, using the same or another input mechanism; and
9. save the accepted sample as visible Chapter 01 evidence only with consent and a delete action.

The tutor must describe uncertainty honestly. If it cannot confidently read the sample, it says that the writing could not be assessed and offers a retry or another input mechanism. If no written-input mechanism is available or accessible, **Continue without writing assessment** remains a technical-failure and accessibility escape hatch; the handwriting objective is marked **Not assessed**, not complete.

### 9.6 Guided conversation — Talk Card

The screen becomes a conversation scene. The tutor represents one speaker and plays or displays one turn at a time.

Rounds:

1. **Echo:** repeat each tutor line.
2. **Complete:** answer three missing responses.
3. **Switch roles:** the pupil asks **బాగున్నారా?**.
4. **Read:** perform from Telugu script without transliteration.

The pupil should always know whose turn it is. While recording, the interface displays a calm listening state and does not animate grades or transcription.

### 9.7 Independent performance — Talk Card

Set a concrete scene:

> You meet a Telugu-speaking teacher for the first time. Greet them, ask how they are, and respond when they ask you back.

Remove transliteration and instruction-language meaning. Permit the pupil to reveal the Telugu lines, but record that the performance was prompted. Save the first completed recording as the Chapter 1 baseline. Offer at most one optional re-recording.

### 9.8 Exit check and reflection — Check Card

Ask the four existing exit checks without showing the source material. Mark each as:

- **Independent** — correct without lesson help;
- **Prompted** — correct after a cue or reveal; or
- **Revisit** — not yet demonstrated.

Then ask:

- How confident would you feel greeting someone this way? (1–5)
- Which part felt hardest? Listening, speaking, reading, writing, or something else?
- Was any instruction confusing?

End with a factual summary, for example:

> You completed the greeting without instruction-language help and recognised మ in నమస్కారం. Next time, we will quickly revisit the long **ā** sound in బా.

## 10. Adaptive tutoring rules

Use the common help ladder and response rules in `common_spec.md`.

### Chapter 01 session adaptation

- If all four expressions are produced independently, shorten repetitive echo practice.
- If comprehension is strong but speech is difficult, spend more time on rhythm and fewer script interactions.
- If speech is strong but script recognition is difficult, keep the dialogue moving and mark letters for later review.
- If the pupil selects the fallback or time runs short, preserve listening, three spoken expressions, five active letters, and one greeting attempt.

## 11. Five-minute fallback flow

The fallback is a legitimate continuity mode, not a completed full lesson. It preserves access to the same five Lesson Cards with reduced content:

1. **Listen:** play the core dialogue once.
2. **Learn:** practise **నమస్కారం**, **బాగున్నారా?**, and **బాగున్నాను**.
3. **Build:** show and trace **న, మ, బ, గ, ర**.
4. **Build:** submit the tracing by image upload, camera, or direct on-screen writing and receive a quick visibility and character-presence check.
5. **Talk:** record or self-perform one greeting attempt.
6. **Check:** save a lesson checkpoint, summarise the available evidence without claiming full completion, and invite the pupil to resume the full lesson later.

The chapter remains **In progress**, with completed fallback work preserved.

## 12. Interface requirements

Use the common lesson layout, interaction states, accessibility requirements, and five-Card Lesson navigation in `common_spec.md`. Identify the current **Listen**, **Learn**, **Build**, **Talk**, or **Check** Card and allow direct navigation to every other accessible Lesson Card.

### Required components

- natural and slow audio player;
- microphone permission and recording controls;
- image upload and camera capture with preview, retake, replace, and delete controls;
- direct-writing surface supporting stylus, finger, and mouse input, with clear, undo, preview, and submit controls;
- Telugu text renderer with reliable combining-mark display;
- optional meaning and transliteration reveal localized for the selected instruction language;
- tutor message and feedback surface;
- dialogue turn indicator;
- script tile and word-building interaction;
- exit-check component;
- session-resume prompt; and
- accessible keyboard alternatives for interactions that require them.

The writing activity must visibly support these states: **choose input method**, **input ready**, **preview**, **checking sample**, **feedback available**, **correction requested**, **accepted**, and **assessment unavailable**.

## 13. Content requirements

The prototype requires:

- natural-speed audio for the complete dialogue and each expression;
- slower teaching audio for each expression;
- an original or licensed illustration/animation of a respectful greeting context;
- canonical Telugu script plus instruction-language-specific transliteration, meaning, usage, and pronunciation guidance for each target expression;
- English default content and a way to provide additional instruction-language variants without changing the Telugu lesson object;
- the complete script map as optional reference content;
- interactive decomposition data for all four expressions;
- handwriting examples and review criteria for the active characters and **నమస్కారం**;
- tutor prompts for an unreadable image or unusable stroke sample, missing writing, recognisable writing, one useful correction, resubmission, acceptance, and unavailable assessment;
- tutor prompts for success, partial success, retry, skip, recording failure, return, and completion;
- a manually reviewed expected-response set for comprehension questions;
- the exit check and reflection prompts.

All Telugu language content and audio should be reviewed by a qualified Telugu speaker before pupil testing.

## 14. Learner progress model

Use the common chapter states, objective statuses, save, resume, restart, and fallback behaviour in `common_spec.md`.

### Per-objective status

Store **Independent**, **Prompted**, **Revisit**, or **Not assessed** for:

- respectful greeting;
- asking how someone is;
- responding and asking back;
- full dialogue performance;
- recognising **మ** and **న**;
- understanding long **ā**; and
- handwriting the active characters and **నమస్కారం**.

## 15. Data and pilot instrumentation

Apply the common data minimisation, consent, and deletion requirements. Chapter 01 additionally records:

- session mode and actual duration;
- selected instruction language and any mid-lesson language change;
- activity reached and completion state;
- replay, slow-audio, meaning, and transliteration use;
- prompt level required for each objective;
- immediate exit-check results;
- confidence before and after the session;
- pupil-reported difficulty, enjoyment, hardest area, and confusing instruction;
- where the pupil paused, exited, or switched to fallback;
- whether the pupil chose to re-record;
- the independent performance recording, with explicit consent;
- writing input mechanism, submitted image or direct-writing strokes, review outcome, retry count, and feedback given, with explicit consent.

## 16. Success measures for the first-pupil test

The prototype is promising when:

- the pupil speaks Telugu within three minutes;
- the full session usually takes 25–35 minutes;
- the pupil completes the independent greeting with no more than one reveal;
- at least five of the seven chapter objectives are Independent or Prompted;
- the pupil submits the required writing through any supported mechanism and can act on one piece of tutor feedback;
- the pupil can recall at least three target expressions one week later without immediately seeing them;
- the pupil reports that the tutor's next action was clear throughout the lesson;
- the pupil can identify at least one piece of feedback that improved a second attempt;
- the pupil is willing to continue to the next lesson;
- the tutor never blocks progress because speech or handwriting assessment, microphone access, or a written-input mechanism fails.

These are pilot thresholds, not final product benchmarks. Revise them after observing the first pupil.

## 17. Functional acceptance criteria

### Guided lesson

- A new pupil can start either the full or fallback session from the welcome screen.
- The tutor plays the dialogue before revealing its meaning in the selected instruction language.
- The pupil is asked to respond in every **Listen**, **Learn**, **Build**, **Talk**, and **Check** Card; no Lesson Card is only passive reading.
- The full route includes all four target expressions, the active script set, guided dialogue, independent performance, and exit check.

### Instruction language

- English is selected by default when the pupil has not chosen another supported instruction language.
- The pupil can choose another supported instruction language before the lesson and change it without losing progress.
- Instructions, explanations, meanings, prompts, feedback, and interface text use the selected instruction language.
- Transliteration uses the selected instruction language's configured script and pronunciation conventions rather than always using the English-default Roman key.
- Changing the instruction language does not change Telugu text, audio, objectives, evidence, or completion status.
- A missing localization is identified as a fallback instead of being silently replaced with English.

### Speech practice

- The pupil can record, replay, retry once, skip, or continue without microphone access.
- Feedback distinguishes an understandable attempt from an unavailable assessment.
- The pupil can complete the lesson when speech analysis is unavailable.

### Handwriting review

- The guided lesson requests **న, మ, స, క, ర, బ, గ** twice and **నమస్కారం** once.
- The pupil can submit the sample by image upload, camera capture, or direct writing with a stylus, finger, or mouse.
- The pupil can preview, retake, replace, clear, undo, resubmit, and delete the sample where those actions apply to the chosen mechanism.
- The pupil can switch input mechanisms without restarting the lesson.
- The tutor checks image or stroke visibility and sample completeness before judging the writing.
- The tutor checks for **న, మ, స, క, ర, బ, గ** and **నమస్కారం**, then gives specific feedback based on the submitted sample.
- The tutor highlights at least one recognisable part before suggesting at most one high-value improvement.
- When a rewrite would help, the tutor requests no more than one corrected sample before continuing.
- An unreadable image, unusable stroke sample, or low-confidence assessment never produces fabricated handwriting feedback.
- If all three written-input mechanisms are unavailable or inaccessible, the pupil may continue and the handwriting objective is marked **Not assessed**.

### Scaffolding

- Meaning, slow audio, and transliteration are initially hidden where specified and can be revealed independently.
- The independent performance begins without transliteration or instruction-language meaning.

### Progress and recovery

- Completing the fallback preserves work and leaves the full lesson available.
- Restarting does not overwrite an earlier baseline recording without confirmation.

## 18. Tutor content examples

### Useful feedback

- “I understood **నమస్కారం**. Try holding the **కా** sound a little longer once.”
- “You used the respectful question correctly.”
- “That answer was understandable. Listen once to the longer **న్న** in the model.”
- “I could not assess that recording clearly. You can retry, replay the model, or continue.”
- “You found **మ** without transliteration.”

### Avoid

- “Wrong pronunciation.”
- “Only 62% accurate.”
- “You failed this exercise.”
- “Perfect!” when the system cannot support that judgment.
- “You broke your streak.”

## 19. First-pupil test script

Use the common testing protocol in `common_spec.md`. For Chapter 01, additionally record:

1. whether the full alphabet reference reassures or overwhelms them; and
2. what greeting expressions and active characters the pupil recalls after one week.

After the session, ask:

- At any point, did this feel like reading a lesson rather than working with a tutor?
- Did the tutor give too much help, too little help, or the right amount?
- Which feedback was useful?
- Which step would you remove or shorten?
- Would you use this tutor for the next chapter?

## 20. Open decisions to resolve through the prototype

- Whether Chapter 01 needs a separate Chapter test, what it assesses beyond the Lesson **Check** Card, and how it is represented without turning the Chapter into a forced workflow.
- Can browser speech recognition assess these four Telugu expressions reliably enough to support broad intelligibility feedback?
- Should natural and slow recordings use one voice or two speakers?
- Does the complete character map belong inside the guided path or only in the reference drawer?
- How accurately can the prototype recognise the active Telugu characters from uploaded images, realistic phone photographs, and direct stroke input, and when must it defer rather than judge?
- Does the pupil prefer a visible tutor character, a voice-only tutor, or a restrained conversational interface?
- Which exact Telugu variety and pronunciation should be the instructional default?
- How much open questioning can the tutor support without distracting from the chapter mission?
- What recording retention period and deletion controls are appropriate for the pilot?

## 21. Prototype release boundary

The first usable release includes one responsive front-end route for Chapter 1, all required lesson content and audio, deterministic tutor branching, local or test-profile progress persistence, recording/replay, image upload, camera capture, direct on-screen writing, handwriting review, graceful failure of microphone or any written-input mechanism, the fallback route, the exit check, and a pilot data export.

Automated pronunciation scoring may be included only if it meets the uncertainty and fallback requirements above. A scripted or rule-based tutor is acceptable for this chapter; the quality of guidance matters more than whether the tutor uses a general-purpose artificial intelligence model.

## 22. Definition of done

Chapter 1 is ready for first-pupil testing when:

- every acceptance criterion has been manually checked;
- all Telugu text, explanations, and recordings have received native-speaker review;
- the complete path and fallback path work on a phone-sized and desktop-sized screen;
- microphone denial, camera denial, unavailable upload, unusable direct input, unreadable images, silent audio, low-confidence assessment, refresh, and interrupted-session cases have been tested;
- the pupil can delete saved recordings, uploaded or captured images, and direct-writing strokes;
- pilot events and reflection answers can be reviewed after the session; and
- a one-week recall check is scheduled or available from the saved chapter state.
