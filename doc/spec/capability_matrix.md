`cap-AUT-0027# Telugu Tutor Capability Matrix

**Status:** Draft capability catalogue  
**Scope:** Technology-neutral capabilities identified from the current course, common tutor, Chapter 01, character-unit, grammar-unit, security, commerce, and entitlement discussions

This document records what the Telugu Tutor product may need to do. It intentionally does not define function signatures, identifiers, assets, storage formats, application architecture, service boundaries, or vendor choices. Those functional and technical requirements come later.

A capability may be small and reusable or composite. The list below groups the capabilities by the product area in which they are used, from instruction and tutoring through evidence, authorization, commerce, security, and safety. Persona definitions and guidance for reading the tables are in the appendices.

The **Computation mode** column classifies how the capability's result is produced:

- **Static** — authored, reviewed, or produced during course or product design and reusable unchanged until its source, review, configuration, or version changes. Static material may be distributed or cached without recomputing it for each learner.
- **Dynamic** — performed, retrieved, recorded, computed, or verified for the current actor, learner response, request, session, or security decision. The result must not be reused as if it were still current.
- **Hybrid** — selects, combines, or presents static material using current learner, session, device, entitlement, or other runtime state.

The classification applies to the capability outcome, not every supporting input. For example, credential material and authorization policy may be cached securely, but authentication and authorization decisions remain **Dynamic** and must be verified for the relevant request. Likewise, learner speech, writing, responses, evidence, progress changes, purchases, and consent decisions are **Dynamic** because they must be retrieved or recorded for the current learner interaction.

A **Static** capability can still be invoked during a lesson. For example, playing an approved recording or showing a localized illustration happens at runtime, but no new instructional content needs to be computed for that learner; the reusable recording or illustration remains static.

Each capability has a canonical identifier in the form `cap-XXX-YYYY`. `XXX` is the registered three-letter code of the capability's original logical group, and `YYYY` is a four-digit sequence allocated within that group. The identifier denotes the capability independently of its current name, wording, section, personas, or computation mode. Once assigned, an identifier must not be renumbered or reused. If a capability is renamed or later moved to another section, it retains its original identifier and group code. If it is retired, its identifier remains reserved. A materially different new capability receives the next unused sequence in the applicable group.

### Capability group-code registry

| Code | Capability group |
|---|---|
| `LNG` | Instruction language and localization |
| `TRL` | Transliteration |
| `LES` | Lesson and session orchestration |
| `COM` | Tutor communication and conduct |
| `ADP` | Adaptive teaching and progressive help |
| `AUD` | Audio presentation |
| `SPC` | Speech collection and understanding |
| `INP` | Image, camera, and direct writing |
| `HWR` | Written-sample review |
| `CHR` | Character and writing-system learning |
| `UNT` | Reusable character and grammar units |
| `GRM` | Grammar, usage, comprehension, and dialogue |
| `PRG` | Evidence, progress, reflection, and recovery |
| `PRV` | Consent, privacy, and accessibility |
| `GOV` | Pilot instrumentation and content governance |
| `AUT` | Identity and ability-based authorization |
| `ENT` | Content entitlement and educational eligibility |
| `CST` | Costly tutor-operation entitlement |
| `BUY` | Catalogue, purchase, and subscription |
| `SEC` | Security and accountability |
| `CHD` | Child and guardian safety |
| `CRS` | Course orientation and structure |

## 1. Instruction language and localization
So instructions or GUI should be assets driven. But transliteration is run time.

| Canonical ID | Name                                      | Definition                                                                                                                                   | Description                                                                                                                                                          | Example personas involved            | Computation mode |
|---| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ | ---------------- |
| cap-LNG-0001 | Select instruction language               | Choose the language used to teach Telugu.                                                                                                    | Applies to onboarding, instructions, explanations, meanings, prompts, feedback, interface text, summaries, and accessibility text. Preference part - 1 time activity | Student                              | Dynamic          |
| cap-LNG-0002 | Apply default instruction language        | Use a declared default when no preference exists.                                                                                            | English is the present pilot default, not a permanent product constraint.                                                                                            | System Tutor                         | Hybrid           |
| cap-LNG-0003 | Change instruction language               | Change teaching language without restarting learning.                                                                                        | The change may occur before or during a lesson.                                                                                                                      | Student                              | Dynamic          |
| cap-LNG-0004 | Remember language preference              | Retain the student's selected instruction language.                                                                                          | Allows later sessions to begin with the established preference.                                                                                                      | Student, System Tutor                | Dynamic          |
| cap-LNG-0005 | Preserve learning across language change  | Keep Telugu content, objectives, evidence, and progress unchanged.                                                                           | Only the teaching-language presentation changes.                                                                                                                     | System Tutor                         | Dynamic          |
| cap-LNG-0006 | Localize onboarding                       | Present setup and orientation in the selected language.                                                                                      | Includes mission, permissions, modes, and introductory guidance.                                                                                                     | Student, System Tutor                | Static           |
| cap-LNG-0007 | Localize instruction                      | Present learning directions in the selected language.                                                                                        | Instructions remain plain and concise.                                                                                                                               | Student, System Tutor                | Static           |
| cap-LNG-0008 | Localize explanation                      | Explain Telugu forms and concepts in the selected language.                                                                                  | Includes grammar, usage, cultural context, and pronunciation guidance.                                                                                               | Student, System Tutor                | Static           |
| cap-LNG-0009 | Localize natural meaning                  | Present the natural meaning of Telugu content.                                                                                               | Meaning is contextual rather than necessarily word-for-word.                                                                                                         | Student, System Tutor                | Static           |
| cap-LNG-0010 | Localize authored prompts                 | Provide localized prompts, directions, hints, and recovery messages prepared as reusable course material.                                    | These instructional assets remain static until the approved language variant changes.                                                                                | Student, System Tutor                | Static           |
| cap-LNG-0011 | Localize response-specific feedback       | Present feedback in the selected instruction language using current learner evidence.                                                        | Localized terminology and templates may be static, but the selected observation and message depend on the current response.                                          | Student, System Tutor                | Hybrid           |
| cap-LNG-0012 | Localize interface and accessibility text | Present controls, states, and assistive labels in the selected language.                                                                     | Covers visible text and nonvisual labels.                                                                                                                            | Student, System Tutor                | Static           |
| cap-LNG-0013 | Provide localized instructional asset     | Supply an approved text, image, illustration, animation, audio explanation, or other teaching resource in the selected instruction language. | The asset is created or reviewed during course design and reused until that localized asset version changes.                                                         | Student, System Tutor, Administrator | Static           |
| cap-LNG-0014 | Select localized asset variant            | Choose the appropriate static instructional or interface asset for the current instruction-language preference and content version.          | Asset variants are static; selection is based on current runtime state.                                                                                              | Student, System Tutor                | Hybrid           |
| cap-LNG-0015 | Increase Telugu progressively             | Use more target-language Telugu as the student advances.                                                                                     | Instruction-language support recedes without changing the outcome.                                                                                                   | Student, System Tutor                | Dynamic          |
| cap-LNG-0016 | Detect missing localization               | Identify unavailable localized content.                                                                                                      | Localization coverage is evaluated against an approved content version and remains reusable until that version changes.                                              | System Tutor, Administrator          | Static           |
| cap-LNG-0017 | Disclose fallback language                | State when another language is being used as fallback.                                                                                       | The product must not silently substitute English.                                                                                                                    | Student, System Tutor                | Dynamic          |
| cap-LNG-0018 | Review localized content                  | Confirm a language variant is accurate and suitable.                                                                                         | Review can cover meaning, terminology, explanation, feedback, and pronunciation approximations.                                                                      | Tutor, Administrator                 | Static           |

## 2. Transliteration
This will need detailed functional thinking - for each character, grammar, word unit - this may  need to be generated runtime? or compile time??

| Canonical ID | Name                                   | Definition                                                                           | Description                                                                                                        | Example personas involved   | Computation mode |
|---| -------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | --------------------------- | ---------------- |
| cap-TRL-0001 | Present adapted transliteration        | Show transliteration appropriate to the selected instruction language.               | It may use a non-Roman script and language-specific spelling conventions.                                          | Student, System Tutor       | Dynamic          |
| cap-TRL-0002 | Adapt pronunciation approximation      | Express Telugu sounds through comparisons useful to the selected language's readers. | English-oriented approximations are only one variant.                                                              | Student, System Tutor       | Dynamic          |
| cap-TRL-0003 | Adapt syllable representation          | Use syllable divisions suitable for the instruction language.                        | Preserves the canonical Telugu expression.                                                                         | Student, System Tutor       | Dynamic          |
| cap-TRL-0004 | Reveal transliteration as help         | Make transliteration available progressively.                                        | Use is assistance, not an error.                                                                                   | Student, System Tutor       | Dynamic          |
| cap-TRL-0005 | Hide transliteration                   | Remove transliteration when it is no longer needed.                                  | Required for suitably independent performance.                                                                     | System Tutor                | Dynamic          |
| cap-TRL-0006 | Detect missing transliteration variant | Identify that no suitable variant exists.                                            | Variant coverage is evaluated against an approved content version and remains reusable until that version changes. | System Tutor, Administrator | Static           |
| cap-TRL-0007 | Review transliteration variant         | Validate script, spelling, sound comparisons, and usability.                         | Review occurs separately for each supported instruction language.                                                  | Tutor, Administrator        | Static           |

## 3. Lesson and session orchestration

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-LES-0001 | Present lesson mission | State the practical communication outcome. | Describes what the student will be able to do, not merely consume. | Student, System Tutor | Static |
| cap-LES-0002 | Start full lesson | Begin the normal guided route. | Chapter 01 targets approximately thirty minutes while adapting to responses. | Student, System Tutor | Dynamic |
| cap-LES-0003 | Start fallback lesson | Begin a legitimate short continuity route. | It preserves essential contact without claiming full completion. | Student, System Tutor | Dynamic |
| cap-LES-0004 | Present one task at a time | Keep a single required action in focus. | Help may remain available without forcing navigation decisions. | Student, System Tutor | Hybrid |
| cap-LES-0005 | Move through lesson activities | Guide the pupil among activities needed for the Lesson objective. | Names such as Listen, Learn, Build, Talk, and Check may be useful to authors, but they are not required phases, a required order, or student-interface labels. | Student, System Tutor | Hybrid |
| cap-LES-0006 | Adjust lesson timing | Vary activity duration using learner evidence. | The practical outcome remains more important than fixed timing. | System Tutor | Dynamic |
| cap-LES-0007 | Preserve essentials when time is short | Retain the most valuable listening, speech, script, and performance work. | Can trigger or shape the fallback route. | Student, System Tutor | Dynamic |
| cap-LES-0008 | Run exit check | Conduct concise evidence checks at the end. | Completion does not require every objective to be independent. | Student, System Tutor | Dynamic |
| cap-LES-0009 | Complete lesson | Record that the exit-check boundary was reached. | Objective statuses remain individually evidence-based. | System Tutor | Dynamic |
| cap-LES-0010 | Complete fallback | Record short-route continuity without full completion. | Completed fallback work remains available later. | System Tutor | Dynamic |
| cap-LES-0011 | Run Chapter 01 full session | **Composite:** conduct the complete greeting lesson. | Coordinates content, audio, speech, script, handwriting, dialogue, assessment, recovery, and summary. | Student, System Tutor | Hybrid |
| cap-LES-0012 | Run Chapter 01 fallback session | **Composite:** conduct the five-minute greeting route. | Coordinates core dialogue, three expressions, five letters, writing evidence, one greeting, and checkpointing. | Student, System Tutor | Hybrid |

## 4. Tutor communication and conduct

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-COM-0001 | Greet student warmly | Open the tutoring interaction constructively. | Tone is welcoming without generic or unsupported celebration. | System Tutor | Static |
| cap-COM-0002 | Give concise instruction | Speak or display short, direct guidance. | Each turn asks for one response or action. | System Tutor | Static |
| cap-COM-0003 | Demonstrate before explaining | Present natural Telugu prior to teaching-language support. | Supports audio-first learning. | System Tutor | Static |
| cap-COM-0004 | Invite contextual inference | Ask the student to predict meaning from scene, tone, or repetition. | Encourages comprehension before translation. | Student, System Tutor | Static |
| cap-COM-0005 | Wait for response | Allow sufficient response time before revealing help. | Distinguishes genuine silence from immediate uncertainty. | System Tutor | Dynamic |
| cap-COM-0006 | Explain usage and social context | Teach when, why, and with whom language is appropriate. | Includes respect, register, tone, and reciprocal behavior. | Student, System Tutor | Static |
| cap-COM-0007 | Give evidence-based praise | Name what the student demonstrably achieved. | Avoids unsupported claims such as perfect performance. | System Tutor | Dynamic |
| cap-COM-0008 | Give focused correction | Offer at most the highest-value pronunciation and language improvements. | Communication is considered before correction. | System Tutor | Dynamic |
| cap-COM-0009 | Answer safe aside briefly | Respond to an off-topic question without losing the lesson mission. | General chat must not replace the chapter objective. | Student, System Tutor | Dynamic |
| cap-COM-0010 | Return to mission | Resume the active learning task after an aside. | Keeps the tutoring route coherent. | System Tutor | Dynamic |
| cap-COM-0011 | Generate learning summary | Describe demonstrated skills and the most useful revisit item. | Summary derives from collected evidence. | Student, System Tutor | Dynamic |
| cap-COM-0012 | Maintain tutor presence | **Composite:** lead, observe, adapt, and gradually withdraw help. | The experience should feel attended to rather than like a static slideshow. | Student, System Tutor | Hybrid |

## 5. Adaptive teaching and progressive help

| Canonical ID | Name                                     | Definition                                                                                                 | Description                                                             | Example personas involved | Computation mode |
|---| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------- | ---------------- |
| cap-ADP-0001 | Classify learner response                | Distinguish success, partial success, valid variation, silence, need for help, and unavailable assessment. | Technical failure is separated from learning difficulty.                | System Tutor              | Dynamic          |
| cap-ADP-0002 | Decide whether to advance                | Move forward when the current task has been sufficiently completed.                                        | Does not force every help step.                                         | System Tutor              | Dynamic          |
| cap-ADP-0003 | Decide whether retry helps               | Offer another attempt only when useful.                                                                    | Repetition is limited after unsuccessful attempts.                      | System Tutor              | Dynamic          |
| cap-ADP-0004 | Offer smaller prompt                     | Reduce a difficult task without giving away everything.                                                    | May isolate a sound, syllable, character, ending, or response fragment. | System Tutor              | Hybrid           |
| cap-ADP-0005 | Replay natural model                     | Repeat the normal spoken example.                                                                          | First level of the help ladder.                                         | Student, System Tutor     | Static           |
| cap-ADP-0006 | Replay slow model                        | Repeat a slower teaching example.                                                                          | Slow playback should retain natural pitch where feasible.               | Student, System Tutor     | Static           |
| cap-ADP-0007 | Reveal Telugu expression                 | Show canonical Telugu script as help.                                                                      | Telugu remains the primary written representation.                      | Student, System Tutor     | Static           |
| cap-ADP-0008 | Highlight relevant feature               | Draw attention to a sound, syllable, character, sign, or ending.                                           | Provides focused rather than broad explanation.                         | Student, System Tutor     | Static           |
| cap-ADP-0009 | Reveal natural meaning                   | Show meaning in the selected instruction language.                                                         | Appears after Telugu exposure or when requested.                        | Student, System Tutor     | Static           |
| cap-ADP-0010 | Provide complete echo model              | Let the student hear and repeat the whole response.                                                        | Final help-ladder step before advancing.                                | Student, System Tutor     | Static           |
| cap-ADP-0011 | Record greatest help used                | Preserve the highest scaffold level used for an objective.                                                 | Supports objective status and pilot analysis.                           | System Tutor              | Dynamic          |
| cap-ADP-0012 | Remove help after success                | Withdraw meaning, transliteration, construction, and model audio progressively.                            | Promotes independent communication.                                     | System Tutor              | Dynamic          |
| cap-ADP-0013 | Shorten mastered practice                | Reduce repetitive echo work after independent production.                                                  | Frees time for higher-value practice.                                   | System Tutor              | Dynamic          |
| cap-ADP-0014 | Rebalance speech and script work         | Allocate attention according to demonstrated strengths and difficulties.                                   | Script difficulty need not stop spoken dialogue, and vice versa.        | System Tutor              | Dynamic          |
| cap-ADP-0015 | Continue after two unsuccessful attempts | Model, echo once, mark for revisit, and move on.                                                           | Prevents trapping or shame.                                             | Student, System Tutor     | Dynamic          |
| cap-ADP-0016 | Continue after unavailable assessment    | Offer retry, self-check, alternative, or continuation.                                                     | Never fabricates a score.                                               | Student, System Tutor     | Dynamic          |
| cap-ADP-0017 | Run adaptive tutor turn                  | **Composite:** observe, classify, help, assess, record, and choose the next action.                        | Central decision-making loop for every responsive activity.             | Student, System Tutor     | Dynamic          |

## 6. Audio presentation

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-AUD-0001 | Play natural Telugu audio | Present a natural expression or dialogue. | Used before meaning or transliteration. | Student, System Tutor | Static |
| cap-AUD-0002 | Play slow Telugu audio | Present a teaching-speed version. | Supports focused imitation without becoming the default model. | Student, System Tutor | Static |
| cap-AUD-0003 | Play dialogue turn | Present one speaker's contribution. | Supports guided conversation and clear turn-taking. | Student, System Tutor | Static |
| cap-AUD-0004 | Replay audio | Repeat previously presented audio. | Student-controlled replay is not penalized. | Student, System Tutor | Static |
| cap-AUD-0005 | Pause audio | Temporarily stop playback. | Supports control and accessibility. | Student | Dynamic |
| cap-AUD-0006 | Resume audio | Continue paused playback. | Preserves the learner's place. | Student | Dynamic |
| cap-AUD-0007 | Stop audio | End current playback. | Keeps the interface responsive to learner choice. | Student, System Tutor | Dynamic |
| cap-AUD-0008 | Control audio level | Adjust audible volume. | Supports device context and accessibility. | Student | Dynamic |
| cap-AUD-0009 | Indicate playback state | Communicate whether audio is ready, playing, paused, or failed. | State must also be accessible nonvisually. | Student, System Tutor | Dynamic |
| cap-AUD-0010 | Check audio readiness | Confirm the student can hear lesson audio. | Includes a short replayable setup check. | Student, System Tutor | Dynamic |
| cap-AUD-0011 | Detect unusable lesson audio | Identify silent, missing, or failed playback. | Enables recovery rather than blocking. | System Tutor, Administrator | Dynamic |
| cap-AUD-0012 | Provide audio text alternative | Make spoken content available as text after the initial listen-first moment. | Supports accessibility without defeating initial inference. | Student, System Tutor | Static |
| cap-AUD-0013 | Speak through device | Present tutor speech using available device audio. | May use recorded or generated speech without prescribing either. | Student, System Tutor | Hybrid |

## 7. Speech collection and understanding

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-SPC-0001 | Request microphone access | Ask in context and explain the purpose. | Includes a continue-without-recording route. | Student, System Tutor | Dynamic |
| cap-SPC-0002 | Capture spoken attempt | Listen to and retain a complete learner utterance for immediate use. | Must not interrupt the student. | Student, System Tutor | Dynamic |
| cap-SPC-0003 | Cancel spoken attempt | Abandon the current capture. | Allows recovery from accidental starts. | Student | Dynamic |
| cap-SPC-0004 | Indicate recording state | Communicate ready, listening, processing, feedback, retry, complete, or unavailable. | Must be visually and nonvisually understandable. | Student, System Tutor | Dynamic |
| cap-SPC-0005 | Detect absent speech | Determine that no usable speech was captured. | Distinct from an incorrect language attempt. | System Tutor | Dynamic |
| cap-SPC-0006 | Detect recording failure | Identify a technical microphone or capture problem. | Leads to retry or alternative rather than correction. | System Tutor | Dynamic |
| cap-SPC-0007 | Replay learner recording | Let the student hear their own attempt. | Supports reflection and self-check. | Student | Dynamic |
| cap-SPC-0008 | Retry spoken attempt | Capture one further attempt when useful. | Tutor limits unproductive repetition. | Student, System Tutor | Dynamic |
| cap-SPC-0009 | Skip recording | Continue without microphone participation. | Enables listen-and-self-rate mode. | Student, System Tutor | Dynamic |
| cap-SPC-0010 | Transcribe speech | Convert spoken language into a textual interpretation when useful. | Raw transcription is not automatically shown or treated as truth. | System Tutor | Dynamic |
| cap-SPC-0011 | Recognize target expression | Determine whether an expected expression was spoken. | Accepts relevant variation where appropriate. | System Tutor | Dynamic |
| cap-SPC-0012 | Assess broad intelligibility | Determine whether the intended message would be understood. | Does not claim precise accent grading. | System Tutor | Dynamic |
| cap-SPC-0013 | Assess contextual appropriateness | Determine whether the spoken form suits the social situation. | Includes respectful usage. | System Tutor | Dynamic |
| cap-SPC-0014 | Notice pronunciation feature | Observe a high-value feature such as vowel length, doubled consonant, rhythm, or question intonation. | Used for one focused improvement. | System Tutor | Dynamic |
| cap-SPC-0015 | Estimate speech-assessment reliability | Decide whether the speech evidence supports a judgment. | Low reliability produces uncertainty rather than a score. | System Tutor | Dynamic |
| cap-SPC-0016 | Withhold unreliable speech judgment | Decline to grade when evidence is insufficient. | Offers replay, retry, self-check, or continuation. | Student, System Tutor | Dynamic |
| cap-SPC-0017 | Generate speech feedback | Describe understandable communication and one useful improvement. | Internal recognition output and confidence values remain hidden. | Student, System Tutor | Dynamic |
| cap-SPC-0018 | Collect speech self-rating | Let the student judge their attempt when automation is skipped or unavailable. | Self-rating does not masquerade as measured assessment. | Student, System Tutor | Dynamic |
| cap-SPC-0019 | Preserve baseline performance | Retain the first complete Chapter 01 greeting with consent. | Optional re-recording must not silently destroy the baseline. | Student, System Tutor | Dynamic |
| cap-SPC-0020 | Store spoken evidence | Retain a recording with explained purpose and consent. | Storage and retention are independently governed. | Student, System Tutor | Dynamic |
| cap-SPC-0021 | Delete spoken evidence | Remove a retained recording. | Available to an actor with the explicit ability. | Student, Administrator | Dynamic |
| cap-SPC-0022 | Assess spoken attempt | **Composite:** capture, validate, interpret, judge reliability, give feedback, and choose continuation. | Learner-facing output emphasizes communication rather than technical scoring. | Student, System Tutor | Dynamic |

## 8. Image, camera, and direct writing

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-INP-0001 | Request camera access | Ask only after camera capture is selected and explain why. | Denial must not block other writing methods. | Student, System Tutor | Dynamic |
| cap-INP-0002 | Show camera preview | Display the writing surface before capture. | Supports positioning and visibility. | Student | Dynamic |
| cap-INP-0003 | Capture writing photograph | Photograph writing completed on a physical surface. | One of three equivalent collection routes. | Student | Dynamic |
| cap-INP-0004 | Select existing writing image | Choose a previously created image from the device. | Remains available when camera use is unsuitable. | Student | Dynamic |
| cap-INP-0005 | Preview writing image | Show the selected or captured image before submission. | Allows informed acceptance or replacement. | Student | Dynamic |
| cap-INP-0006 | Retake photograph | Replace a camera capture with a new one. | Does not restart the lesson. | Student | Dynamic |
| cap-INP-0007 | Replace writing image | Substitute a different uploaded image. | Preserves activity state. | Student | Dynamic |
| cap-INP-0008 | Delete writing image | Remove a captured or uploaded sample. | Applies both before and after accepted storage as authorized. | Student, Administrator | Dynamic |
| cap-INP-0009 | Validate image usability | Check format, visibility, focus, lighting, and completeness. | Occurs before handwriting judgment. | System Tutor | Dynamic |
| cap-INP-0010 | Provide writing surface | Allow direct writing with finger, stylus, mouse, or other pointer. | Input tool is not part of language proficiency. | Student, System Tutor | Dynamic |
| cap-INP-0011 | Capture original strokes | Preserve the sequence of direct-writing marks. | Supports undo, replay, and later analysis with consent. | Student, System Tutor | Dynamic |
| cap-INP-0012 | Prevent accidental scrolling | Keep page movement from interfering with writing. | Maintains a usable drawing surface. | Student, System Tutor | Dynamic |
| cap-INP-0013 | Undo writing stroke | Remove the most recent mark. | Supports correction before submission. | Student | Dynamic |
| cap-INP-0014 | Clear writing surface | Remove the current direct-writing sample. | Allows a fresh attempt. | Student | Dynamic |
| cap-INP-0015 | Preview direct writing | Show the captured strokes before submission. | Equivalent to image preview. | Student | Dynamic |
| cap-INP-0016 | Replay writing strokes | Reproduce the writing sequence. | Available when original strokes were captured and retained. | Student, System Tutor | Dynamic |
| cap-INP-0017 | Switch writing method | Move among upload, camera, and direct writing without restarting. | Existing lesson progress is preserved. | Student, System Tutor | Dynamic |

## 9. Written-sample review

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-HWR-0001 | State writing request | Specify exactly which characters or words to write. | Chapter 01 requests active characters twice and నమస్కారం once. | Student, System Tutor | Static |
| cap-HWR-0002 | Collect written sample | Accept upload, photograph, or direct writing through one common loop. | Methods produce equivalent objective treatment. | Student, System Tutor | Dynamic |
| cap-HWR-0003 | Check sample completeness | Confirm enough requested writing is present. | Missing content is addressed before form judgment. | System Tutor | Dynamic |
| cap-HWR-0004 | Recognize Telugu characters | Identify likely characters in a submitted sample. | Recognition remains uncertainty-aware. | System Tutor | Dynamic |
| cap-HWR-0005 | Detect expected characters | Check whether the requested active set appears. | Chapter 01 includes న, మ, స, క, ర, బ, గ. | System Tutor | Dynamic |
| cap-HWR-0006 | Detect expected word | Check whether a requested Telugu word appears. | Chapter 01 specifically checks నమస్కారం. | System Tutor | Dynamic |
| cap-HWR-0007 | Identify recognisable writing | Name at least one successful part of the sample. | Positive evidence precedes correction. | Student, System Tutor | Dynamic |
| cap-HWR-0008 | Notice handwriting feature | Observe proportions, vowel-sign placement, completeness, or legibility. | Used only when supported by the sample. | System Tutor | Dynamic |
| cap-HWR-0009 | Estimate handwriting-assessment reliability | Decide whether the sample can be judged. | Unreadable or unusable evidence is not graded. | System Tutor | Dynamic |
| cap-HWR-0010 | Withhold unreliable handwriting judgment | State uncertainty and offer retry, another method, or continuation. | Prevents fabricated handwriting feedback. | Student, System Tutor | Dynamic |
| cap-HWR-0011 | Select handwriting improvement | Choose at most one high-value correction. | Avoids overwhelming the learner. | System Tutor | Dynamic |
| cap-HWR-0012 | Request corrected writing | Ask for no more than one revised sample when useful. | May use the same or a different input method. | Student, System Tutor | Dynamic |
| cap-HWR-0013 | Generate handwriting feedback | Describe recognisable work and the selected improvement. | Feedback is specific to submitted evidence. | Student, System Tutor | Dynamic |
| cap-HWR-0014 | Mark writing not assessed | Record that technical or accessibility limitations prevented assessment. | Does not count the objective as complete. | System Tutor | Dynamic |
| cap-HWR-0015 | Store writing evidence | Retain accepted images or strokes with consent. | Includes purpose explanation and deletion. | Student, System Tutor | Dynamic |
| cap-HWR-0016 | Delete writing evidence | Remove retained photographs, images, or strokes. | Does not automatically erase nonsensitive progress. | Student, Administrator | Dynamic |
| cap-HWR-0017 | Review handwriting sample | **Composite:** collect, validate, recognize, judge reliability, give feedback, and continue. | Shared across all supported input methods. | Student, System Tutor | Dynamic |

## 10. Character and writing-system learning

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-CHR-0001 | Present character map | Show the complete Telugu writing system as optional orientation. | It is not automatically an active test. | Student, System Tutor | Static |
| cap-CHR-0002 | Present focused character set | Limit active work to the forms used by the lesson. | Chapter 01 focuses on seven consonants and selected signs and combinations. | Student, System Tutor | Static |
| cap-CHR-0003 | Explain character sound | Connect a Telugu form to its sound. | Guidance may vary by instruction language. | Student, System Tutor | Static |
| cap-CHR-0004 | Explain writing function | Describe what a character, sign, or mark does. | Includes inherent vowels, vowel signs, virāma, and anusvāra. | Student, System Tutor | Static |
| cap-CHR-0005 | Decompose combined form | Show the ordered components of a composite form. | Components remain independently teachable. | Student, System Tutor | Static |
| cap-CHR-0006 | Compose combined form | Show how components form a new written unit. | Supports conjunct and doubled forms. | Student, System Tutor | Static |
| cap-CHR-0007 | Connect script to speech | Link written forms to expressions the student already hears and says. | Spoken-first does not mean spoken-only. | Student, System Tutor | Static |
| cap-CHR-0008 | Match sound and word | Choose the written expression corresponding to heard audio. | Produces recognition evidence. | Student, System Tutor | Dynamic |
| cap-CHR-0009 | Assemble Telugu word | Arrange written components in the expected sequence. | Chapter 01 builds greeting words interactively. | Student, System Tutor | Dynamic |
| cap-CHR-0010 | Locate character in word | Find a target form inside a familiar expression. | Chapter 01 assesses recognition of మ and న. | Student, System Tutor | Dynamic |
| cap-CHR-0011 | Contrast written endings | Highlight differences between related expressions. | Supports question-answer distinctions. | Student, System Tutor | Dynamic |
| cap-CHR-0012 | Transform base with sign | Demonstrate and test how a sign changes a consonant. | Chapter 01 assesses the long ā sign. | Student, System Tutor | Dynamic |
| cap-CHR-0013 | Assess character recognition | Determine whether the student identifies an active form. | Records independent, prompted, revisit, or not assessed. | System Tutor | Dynamic |

## 11. Reusable character and grammar units

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-UNT-0001 | Retrieve character unit | Access one coherent character-learning object independently. | Unit identity does not depend on a chapter. | System Tutor, Administrator | Static |
| cap-UNT-0002 | Retrieve grammar unit | Access one coherent grammar or usage object independently. | Unit identity does not depend on a chapter. | System Tutor, Administrator | Static |
| cap-UNT-0003 | Represent atomic unit | Describe a smallest independently useful learning object. | Exact future taxonomy remains open. | Administrator | Static |
| cap-UNT-0004 | Represent composite unit | Describe a reusable object through ordered component relationships. | The composite is accessible independently of its components. | System Tutor, Administrator | Static |
| cap-UNT-0005 | Traverse unit components | Move between a composite and its constituent units. | Enables teaching or assessment at either level. | System Tutor, Administrator | Static |
| cap-UNT-0006 | Describe unit properties | Provide canonical form or pattern, category, purpose, guidance, examples, and metadata as applicable. | Property requirements may differ by unit type. | System Tutor, Administrator | Static |
| cap-UNT-0007 | Describe unit prerequisites | Identify learning objects useful before a unit. | Does not itself impose commercial access. | Student, System Tutor | Static |
| cap-UNT-0008 | Describe related units and variants | Connect useful alternatives, contrasts, and forms. | Supports curriculum navigation and explanation. | System Tutor, Administrator | Static |
| cap-UNT-0009 | Provide unit media and accessibility information | Associate suitable presentation and accessible guidance. | Does not prescribe storage representation. | Student, System Tutor, Administrator | Static |
| cap-UNT-0010 | Localize character unit guidance | Vary accessible names, explanations, approximations, and transliteration. | Canonical Telugu form remains unchanged. | Student, System Tutor, Administrator | Static |
| cap-UNT-0011 | Localize grammar unit guidance | Vary name, meaning, explanation, terminology, examples, and transliteration. | Canonical Telugu pattern remains unchanged. | Student, System Tutor, Administrator | Static |
| cap-UNT-0012 | Reference unit from lesson | Relate a lesson to a unit as orientation, notice, introduction, practice, reinforcement, or assessment. | Contextual examples and evidence belong to the lesson. | System Tutor, Administrator | Static |
| cap-UNT-0013 | Reuse unit across lessons | Share canonical learning content without chapter-specific progress inside the unit. | Avoids duplication and hidden backlinks. | System Tutor, Administrator | Static |
| cap-UNT-0014 | Protect lesson from unit change | Prevent a shared-unit update from silently changing an existing lesson outcome. | Requires review or compatible version handling. | Administrator | Static |
| cap-UNT-0015 | Validate unit composition | Confirm component references and relationships are coherent. | Applies to character and grammar composites. | System Tutor, Administrator | Static |

## 12. Grammar, usage, comprehension, and dialogue

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-GRM-0001 | Teach useful whole pattern | Present an expression or exchange before a full grammar analysis. | Chapter 01 teaches greeting forms as communicative wholes. | Student, System Tutor | Static |
| cap-GRM-0002 | Explain respectful usage | Describe forms suitable for an elder, teacher, or unfamiliar adult. | Includes నమస్కారం, బాగున్నారా?, and మీరు?. | Student, System Tutor | Static |
| cap-GRM-0003 | Explain dialogue pattern | Describe greet, ask, answer, and ask-back structure. | Supports communicative assembly. | Student, System Tutor | Static |
| cap-GRM-0004 | Explain grammar contrast | Clarify meaningful differences between forms. | Chapter 01 contrasts question and first-person endings. | Student, System Tutor | Static |
| cap-GRM-0005 | Present common mistake | Show a likely misuse or confusing contrast. | Kept relevant to the active mission. | Student, System Tutor | Static |
| cap-GRM-0006 | Assess usage choice | Determine whether a selected form suits the context. | Focuses on respectful greeting usage in Chapter 01. | System Tutor | Dynamic |
| cap-GRM-0007 | Ask contextual comprehension | Test situation, repetition, question sound, or natural meaning one item at a time. | Audio precedes explanation. | Student, System Tutor | Dynamic |
| cap-GRM-0008 | Accept equivalent comprehension answer | Recognize semantically valid wording. | Avoids exact-string grading. | System Tutor | Dynamic |
| cap-GRM-0009 | Conduct listen-and-infer activity | **Composite:** play context, ask focused questions, evaluate, and reveal help progressively. | Captures comprehension without beginning with translation. | Student, System Tutor | Hybrid |
| cap-GRM-0010 | Present dialogue scene | Establish speakers, context, and current turn. | Turn state cannot rely on color alone. | Student, System Tutor | Static |
| cap-GRM-0011 | Conduct echo round | Ask the student to repeat each model line. | Early guided production. | Student, System Tutor | Dynamic |
| cap-GRM-0012 | Conduct completion round | Ask the student to supply missing responses. | Reduces model dependence. | Student, System Tutor | Dynamic |
| cap-GRM-0013 | Conduct role-switch round | Have the student initiate the respectful question. | Tests flexible use rather than fixed repetition. | Student, System Tutor | Dynamic |
| cap-GRM-0014 | Conduct script-reading round | Perform from Telugu script without transliteration. | Connects familiar speech to reading. | Student, System Tutor | Dynamic |
| cap-GRM-0015 | Run guided conversation | **Composite:** manage turns, prompts, role changes, recording, and line-level evidence. | Student always knows whose turn it is. | Student, System Tutor | Hybrid |
| cap-GRM-0016 | Run independent performance | **Composite:** set a real scene, remove support, listen, permit a recorded reveal, and assess evidence. | Chapter 01 ends with a complete respectful greeting. | Student, System Tutor | Hybrid |

## 13. Evidence, progress, reflection, and recovery

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-PRG-0001 | Retrieve learner response | Make the learner's current or previously retained response available to the authorized lesson, assessment, recovery, or review activity that needs it. | Applies across comprehension answers, speech, dialogue, writing, reflection, and other response forms; the relevant response and current authorization must be resolved at runtime. | Student, System Tutor | Dynamic |
| cap-PRG-0002 | Store learner response | Preserve a learner response with its activity, learner, timing, consent, and evidence context when retention is allowed. | A response is learner-specific runtime data; reusable course content must not be substituted for it. | Student, System Tutor | Dynamic |
| cap-PRG-0003 | Record objective evidence | Preserve what demonstrates a learning objective. | Evidence may come from comprehension, speech, dialogue, script, or writing. | System Tutor | Dynamic |
| cap-PRG-0004 | Assign objective status | Mark Independent, Prompted, Revisit, or Not assessed. | Status reflects evidence and help used. | System Tutor | Dynamic |
| cap-PRG-0005 | Compare attempts | Identify a meaningful change between initial and corrected work. | Supports evidence-based feedback and pilot learning. | Student, System Tutor | Dynamic |
| cap-PRG-0006 | Identify revisit needs | Find objectives that merit future practice. | Used in summaries and return paths. | Student, System Tutor | Dynamic |
| cap-PRG-0007 | Save activity progress | Preserve completion after every activity. | Refresh or exit must not erase completed work. | Student, System Tutor | Dynamic |
| cap-PRG-0008 | Pause session | Stop temporarily at a sensible checkpoint. | Records the current activity. | Student | Dynamic |
| cap-PRG-0009 | Exit session | Leave while preserving completed work. | Avoids punitive messaging. | Student | Dynamic |
| cap-PRG-0010 | Resume short interruption | Continue at the current activity. | Used when recall loss is unlikely. | Student, System Tutor | Dynamic |
| cap-PRG-0011 | Resume long interruption | Begin with a brief recall check, then resume or revisit. | Applies after a day or more. | Student, System Tutor | Dynamic |
| cap-PRG-0012 | Restart chapter safely | Begin again without silently deleting earlier baseline evidence. | Explicit evidence replacement can be handled separately. | Student, System Tutor | Dynamic |
| cap-PRG-0013 | Preserve fallback work | Carry completed short-route work into the full lesson. | Prevents duplicate effort. | Student, System Tutor | Dynamic |
| cap-PRG-0014 | Recover processing timeout | Exit a stalled assessment state without losing the response. | Offers retry, alternative, or continuation. | Student, System Tutor | Dynamic |
| cap-PRG-0015 | Generate return recap | Summarize prior work and the next sensible action. | Uses welcoming, nonpunitive language. | Student, System Tutor | Dynamic |
| cap-PRG-0016 | Collect learner confidence | Ask for confidence before or after learning. | Used as reflection, not proficiency proof. | Student, System Tutor | Dynamic |
| cap-PRG-0017 | Collect learner experience report | Ask about difficulty, enjoyment, hardest area, confusing instructions, and useful feedback. | Supports course validation. | Student, System Tutor | Dynamic |
| cap-PRG-0018 | Schedule recall check | Make a later retention check available. | Chapter 01 includes a one-week recall goal. | Student, System Tutor | Dynamic |
| cap-PRG-0019 | Run recall check | Ask for expressions and characters without immediate source display. | Produces retention evidence. | Student, System Tutor | Dynamic |

## 14. Consent, privacy, and accessibility

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-PRV-0001 | Explain evidence use | State why sensitive learner evidence may be retained. | Applies to audio, images, photographs, and strokes. | Student, System Tutor | Static |
| cap-PRV-0002 | Request evidence consent | Obtain an explicit decision before storage. | Refusal must not prevent lesson continuation. | Student, System Tutor | Dynamic |
| cap-PRV-0003 | Record consent decision | Preserve the scope and outcome of consent. | Later storage and access depend on it. | Student, System Tutor | Dynamic |
| cap-PRV-0004 | List saved evidence | Show what sensitive evidence is retained. | Supports informed deletion and review. | Student, Administrator | Dynamic |
| cap-PRV-0005 | Delete sensitive evidence | Remove retained recordings, images, or strokes. | Access requires an explicit granted ability. | Student, Administrator | Dynamic |
| cap-PRV-0006 | Apply retention policy | Remove or retain evidence according to the declared period. | Policies may vary by evidence purpose and audience. | System Tutor, Administrator | Dynamic |
| cap-PRV-0007 | Export learner data | Provide an authorized copy of learner information. | Includes appropriate privacy filtering. | Student, Administrator | Dynamic |
| cap-PRV-0008 | Minimize collected data | Retain only what is needed for learning and product evaluation. | Time spent is not the primary success measure. | System Tutor, Administrator | Dynamic |
| cap-PRV-0009 | Provide keyboard operation | Make the lesson operable without pointer-only interaction. | Includes visible focus. | Student, System Tutor | Dynamic |
| cap-PRV-0010 | Provide screen-reader semantics | Label controls, states, dialogue turns, recording, and feedback. | Labels follow the selected instruction language. | Student, System Tutor | Dynamic |
| cap-PRV-0011 | Avoid color-only meaning | Communicate correctness and state through additional cues. | Applies throughout lesson and feedback interfaces. | Student, System Tutor | Dynamic |
| cap-PRV-0012 | Provide non-drag alternative | Offer an accessible way to complete every drag interaction. | Equivalent learning evidence is required. | Student, System Tutor | Dynamic |
| cap-PRV-0013 | Provide accessible writing route | Offer upload, camera, direct input, or equivalent route based on need. | Physical tool is not assessed as language proficiency. | Student, System Tutor | Dynamic |
| cap-PRV-0014 | Render Telugu legibly | Display signs, conjuncts, and active forms at distinguishable sizes. | Applies across supported screen sizes. | Student, System Tutor | Dynamic |
| cap-PRV-0015 | Validate lesson accessibility | **Composite:** check keyboard, assistive labels, noncolor cues, alternatives, language, and screen rendering. | Performed before pupil testing. | System Tutor, Administrator | Dynamic |

## 15. Pilot instrumentation and content governance

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-GOV-0001 | Record session facts | Capture mode, duration, activity reached, and completion state. | Supports pilot review rather than learner scoring. | System Tutor, Administrator | Dynamic |
| cap-GOV-0002 | Record scaffold use | Capture replay, slow audio, meaning, transliteration, and prompt levels. | Reveals where teaching support was needed. | System Tutor, Administrator | Dynamic |
| cap-GOV-0003 | Record recovery events | Capture pause, exit, fallback, retry, rerecord, and resume. | Helps identify friction and continuity needs. | System Tutor, Administrator | Dynamic |
| cap-GOV-0004 | Record writing-review facts | Capture input method, outcome, retry count, and feedback. | Raw evidence is retained only with consent. | System Tutor, Administrator | Dynamic |
| cap-GOV-0005 | Record instruction-language use | Capture the selected language and mid-lesson changes. | Helps validate localization behavior. | System Tutor, Administrator | Dynamic |
| cap-GOV-0006 | Export pilot observations | Make authorized pilot data reviewable. | Excludes unnecessary sensitive content. | Administrator | Dynamic |
| cap-GOV-0007 | Calculate pilot measures | Summarize timing, completion, demonstrated objectives, recall, clarity, improvement, and willingness to continue. | Thresholds remain provisional. | System Tutor, Administrator | Dynamic |
| cap-GOV-0008 | Prepare pilot review | **Composite:** combine events, evidence, reflection, and follow-up observations. | Supports decisions about revising the course and tutor. | Administrator | Dynamic |
| cap-GOV-0009 | Review canonical Telugu | Confirm text, explanation, and audio with a qualified Telugu speaker. | Required before pupil testing. | Tutor, Administrator | Static |
| cap-GOV-0010 | Manage content revision | Create, compare, review, approve, publish, withdraw, or restore content versions as authorized. | Draft content remains distinct from published content. | Administrator | Dynamic |
| cap-GOV-0011 | Validate lesson references | Check links to character and grammar units and their teaching relationships. | Prevents inconsistent reusable content. | System Tutor, Administrator | Static |
| cap-GOV-0012 | Validate complete lesson paths | Check full, fallback, permissions, failures, refresh, resume, consent, deletion, phone, and desktop paths. | Performed before first-pupil testing. | System Tutor, Administrator | Static |

## 16. Identity and ability-based authorization

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-AUT-0001 | Use guest learning identity | Begin without a permanent account. | Guest progress may later be transferred to a persistent identity. | Student | Dynamic |
| cap-AUT-0002 | Create account | Establish a persistent identity. | Does not itself grant paid content or administrative abilities. | Student, Administrator | Dynamic |
| cap-AUT-0003 | Sign in | Prove control of an existing identity. | Authentication is separate from authorization. | Student, Administrator | Dynamic |
| cap-AUT-0004 | Sign out | End the current authenticated session. | Does not erase progress or entitlements. | Student, Administrator | Dynamic |
| cap-AUT-0005 | Recover account access | Restore control through an approved verification path. | Sensitive recovery actions may require stronger proof. | Student, Administrator | Dynamic |
| cap-AUT-0006 | Manage authenticated sessions | Review or end active sign-ins. | Helps contain lost or compromised access. | Student, Administrator | Dynamic |
| cap-AUT-0007 | Export account information | Provide an authorized copy of identity, profile, purchase, entitlement, and account records. | Complements learning-data export without assuming that account and learning records are stored together. | Student, Administrator | Dynamic |
| cap-AUT-0008 | Delete account | Remove an account and apply the declared handling for associated profiles, evidence, purchases, and retained legal records. | The effect on each data category must be explained before confirmation; this capability does not prescribe the later deletion policy. | Student, Administrator | Dynamic |
| cap-AUT-0009 | Maintain learner profiles | Keep learning progress separated for distinct students. | One account may manage more than one profile when explicitly allowed. | Student | Dynamic |
| cap-AUT-0010 | Transfer guest progress | Attach guest learning evidence to a persistent profile. | Prevents loss when registration occurs later. | Student, System Tutor | Dynamic |
| cap-AUT-0011 | Identify trusted automated test actor | Recognize a test actor that was explicitly registered or marked as automated. | This supports test isolation only and remains distinct from detecting undeclared automation. | Automated Agent, System Tutor, Administrator | Dynamic |
| cap-AUT-0012 | Detect suspected automated agent | Identify signals indicating that an interaction may be controlled by an AI or other automated agent. | Detection is probabilistic and may produce false positives or false negatives. It is not identity proof and does not replace ability authorization or abuse protection. | Automated Agent, System Tutor, Administrator | Dynamic |
| cap-AUT-0013 | Grant synthetic-test ability | Permit an explicitly identified automated test actor to exercise a declared part of the learner experience. | Access remains limited by the same fine-grained ability model used for every actor. | System Tutor, Administrator | Dynamic |
| cap-AUT-0014 | Isolate synthetic learner activity | Keep automated test sessions separate from real learner profiles, evidence, progress, purchases, and pilot measures. | Synthetic activity remains attributable to the test actor and cannot be mistaken for human learning evidence. | Automated Agent, System Tutor, Administrator | Dynamic |
| cap-AUT-0015 | Exercise authorized learner journey | Allow a trusted automated test actor to traverse only the student-facing content and operations for which it has explicit abilities. | This supports testing without bypassing content entitlement, costly-capability entitlement, consent boundaries, or other authorization checks. | Automated Agent, System Tutor, Administrator | Dynamic |
| cap-AUT-0016 | Provide tailored simplified automated-agent tutorial | Make a deliberately limited and simplified tutorial experience available for an automated agent. | The tutorial may use content, progression, adaptation, and evidence rules tailored for automated interaction. The exact restrictions and teaching behavior belong in later functional requirements. | Automated Agent, System Tutor, Administrator | Hybrid |
| cap-AUT-0017 | Route suspected automated agent | **Composite:** use the declared automated-agent policy to choose between the normal authorized experience and a tailored simplified tutorial. | A detection signal may inform routing, but safeguards must address uncertainty before changing a human student's experience or an actor's purchased access. | Automated Agent, System Tutor, Administrator | Hybrid |
| cap-AUT-0018 | Grant ability | Add one explicit permission to an actor. | Abilities may concern content, tutor operations, evidence, publishing, commerce, or security. | Administrator, System Tutor | Dynamic |
| cap-AUT-0019 | Revoke ability | Remove an explicit permission. | Must not remove unrelated abilities. | Administrator, System Tutor | Dynamic |
| cap-AUT-0020 | Inspect granted abilities | Determine which abilities an actor currently holds. | Personas do not imply abilities. | Student, System Tutor, Administrator | Dynamic |
| cap-AUT-0021 | Evaluate ability authorization | Determine whether an actor may perform the requested action. | Considers applicable resource, learner, time, uses, and other declared boundaries. | System Tutor | Dynamic |
| cap-AUT-0022 | Refuse unauthorized action | Prevent an action not covered by a valid ability. | Explanation must not expose protected information. | System Tutor | Dynamic |
| cap-AUT-0023 | Grant temporary ability | Permit an action until a declared expiry. | Useful for trials, sponsored access, or time-bound review. | Administrator, System Tutor | Dynamic |
| cap-AUT-0024 | Grant usage-limited ability | Permit a costly operation a declared number of times. | Ability and remaining allowance are distinct facts. | System Tutor, Administrator | Dynamic |
| cap-AUT-0025 | Restore ability | Reinstate a valid ability after purchase restoration or correction. | Prior progress remains available. | System Tutor, Administrator | Dynamic |
| cap-AUT-0026 | Record ability history | Preserve grant, use, expiry, and revocation events. | Supports explanation, reconciliation, and security audit. | System Tutor, Administrator | Dynamic |
| cap-AUT-0027 | Build extensible student profile | Create or extend a student's learning profile using only information needed by current capabilities. | The profile can gain declared attributes later without speculative collection now. The adult pilot does not require age; selected instruction language and accessibility preferences may be retained when supplied. | Student, System Tutor | Dynamic |

## 17. Content entitlement and educational eligibility

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-ENT-0001 | Classify content access | Mark content as free, preview, paid, invitation-only, pilot-only, assigned, coming soon, unavailable, or retired. | Classification can exist at multiple granularities. | Administrator | Static |
| cap-ENT-0002 | Grant course access | Permit use of an entire course. | Commercial packaging expands into explicit abilities. | System Tutor, Administrator | Dynamic |
| cap-ENT-0003 | Grant chapter access | Permit use of one or more chapters. | Does not imply mastery of prerequisites. | System Tutor, Administrator | Dynamic |
| cap-ENT-0004 | Grant lesson access | Permit use of a specific lesson. | Supports fine-grained purchase or assignment. | System Tutor, Administrator | Dynamic |
| cap-ENT-0005 | Grant activity or unit access | Permit use of a specific activity, assessment, character unit, grammar unit, dialogue, media item, or revision pack. | Enables increasingly fine-grained resources. | System Tutor, Administrator | Dynamic |
| cap-ENT-0006 | Grant supplementary-content access | Permit additional practice, recall checks, or media. | May be independent of core chapter access. | System Tutor, Administrator | Dynamic |
| cap-ENT-0007 | Check content entitlement | Determine whether the student currently holds the needed content ability. | Rechecked before protected content is presented. | Student, System Tutor | Dynamic |
| cap-ENT-0008 | Explain locked content | State why content is unavailable and how access may be obtained. | Separates commercial lock from learning recommendation. | Student, System Tutor | Dynamic |
| cap-ENT-0009 | Revoke or expire content access | End an applicable content ability. | Preserves progress for possible later restoration. | System Tutor, Administrator | Dynamic |
| cap-ENT-0010 | Restore content access | Reapply valid purchased, assigned, or complimentary abilities. | Makes preserved progress usable again. | System Tutor, Administrator | Dynamic |
| cap-ENT-0011 | Check educational prerequisite | Determine whether earlier learning is recommended or required. | Kept separate from commercial ownership. | Student, System Tutor | Dynamic |
| cap-ENT-0012 | Explain readiness recommendation | Suggest earlier learning without claiming the student lacks ownership. | A paid lesson may remain visible while not yet recommended. | Student, System Tutor | Dynamic |
| cap-ENT-0013 | Authorize content use | **Composite:** authenticate, inspect abilities, check content scope and validity, and permit or refuse access. | No role lookup is part of the principle. | System Tutor | Dynamic |

## 18. Costly tutor-operation entitlement

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-CST-0001 | Entitle advanced speech assessment | Permit use of higher-cost speech interpretation or feedback. | Can be scoped by lesson, chapter, time, or uses. | System Tutor, Administrator | Dynamic |
| cap-CST-0002 | Entitle transcription | Permit conversion of spoken attempts into text. | Separate from basic recording or playback. | System Tutor, Administrator | Dynamic |
| cap-CST-0003 | Entitle advanced pronunciation feedback | Permit deeper pronunciation analysis. | Must still obey uncertainty rules. | System Tutor, Administrator | Dynamic |
| cap-CST-0004 | Entitle automated handwriting review | Permit character recognition and feedback on writing evidence. | Can be independent of basic writing submission. | System Tutor, Administrator | Dynamic |
| cap-CST-0005 | Entitle generated practice | Permit creation of additional personalized activities. | Can be bounded by use or content scope. | System Tutor, Administrator | Dynamic |
| cap-CST-0006 | Entitle open-ended tutor interaction | Permit broader tutor conversation beyond deterministic lesson turns. | Must not replace the chapter objective. | System Tutor, Administrator | Dynamic |
| cap-CST-0007 | Entitle evidence storage | Permit retained audio, images, or strokes within consent and allowance. | Storage access is separate from assessment access. | System Tutor, Administrator | Dynamic |
| cap-CST-0008 | Entitle detailed progress report | Permit generation or export of richer learning analysis. | Evidence privacy remains separately authorized. | System Tutor, Administrator | Dynamic |
| cap-CST-0009 | Entitle premium localization | Permit an additional instruction-language presentation where commercially offered. | Canonical Telugu and earned progress remain unchanged. | System Tutor, Administrator | Dynamic |
| cap-CST-0010 | Track ability allowance | Determine remaining uses or capacity for a costly capability. | Exhaustion does not erase the underlying learning progress. | Student, System Tutor, Administrator | Dynamic |

## 19. Catalogue, purchase, and subscription

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-BUY-0001 | Present content catalogue | Show available courses, chapters, lessons, bundles, previews, outcomes, prerequisites, languages, and ownership. | Distinguishes purchasable, owned, assigned, and coming-soon content. | Student, Administrator | Hybrid |
| cap-BUY-0002 | Present offer | Explain price, currency, duration, included abilities, and applicable conditions. | Commercial package is not an authorization role. | Student, Administrator | Hybrid |
| cap-BUY-0003 | Check offer eligibility | Determine whether a promotion, regional offer, sponsored grant, or upgrade applies. | Prevents invalid or repeated use. | Student, System Tutor, Administrator | Dynamic |
| cap-BUY-0004 | Buy lesson | Acquire the abilities packaged with an individual lesson. | Supports basic or advanced lessons. | Student | Dynamic |
| cap-BUY-0005 | Buy chapter | Acquire the abilities packaged with a chapter. | Package may include content and bounded costly operations. | Student | Dynamic |
| cap-BUY-0006 | Buy course or bundle | Acquire abilities covering multiple learning resources. | Existing abilities should not be needlessly duplicated. | Student | Dynamic |
| cap-BUY-0007 | Review purchase | Confirm content, abilities, price, charges, and access duration before payment. | Supports informed confirmation. | Student | Dynamic |
| cap-BUY-0008 | Complete purchase | Finalize payment and assign the confirmed abilities. | Must be safe against duplication and interruption. | Student, System Tutor | Dynamic |
| cap-BUY-0009 | Handle interrupted purchase | Reconcile pending or delayed outcomes. | Avoids both duplicate charge and incorrect access. | Student, System Tutor, Administrator | Dynamic |
| cap-BUY-0010 | Provide purchase history | Show completed purchases and their resulting access. | Protected from unauthorized viewing. | Student, Administrator | Dynamic |
| cap-BUY-0011 | Restore purchase | Reconstruct abilities from an earlier valid purchase. | Useful across devices or after reconciliation. | Student, System Tutor, Administrator | Dynamic |
| cap-BUY-0012 | Refund purchase | Reverse an authorized transaction and adjust only the affected abilities. | Preserves abilities obtained elsewhere and retains learning progress. | Student, Administrator | Dynamic |
| cap-BUY-0013 | Start subscription | Grant the abilities contained in a recurring access offer. | Optional commercial model. | Student | Dynamic |
| cap-BUY-0014 | Manage subscription | Renew, change, cancel renewal, apply grace, or restore access. | Separately purchased permanent content remains unaffected. | Student, System Tutor, Administrator | Dynamic |
| cap-BUY-0015 | Reconcile commerce and abilities | **Composite:** ensure confirmed purchases, refunds, subscriptions, and assigned abilities agree. | Corrects missing, duplicate, expired, or conflicting grants. | System Tutor, Administrator | Dynamic |

## 20. Security and accountability

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-SEC-0001 | Protect information in transit | Prevent unauthorized observation or alteration while information moves. | Applies to learning, identity, commerce, and content data. | System Tutor, Administrator | Dynamic |
| cap-SEC-0002 | Protect stored sensitive information | Prevent unauthorized access to retained evidence, identity, and commerce data. | Storage method remains unspecified. | System Tutor, Administrator | Dynamic |
| cap-SEC-0003 | Validate received input | Reject malformed or dangerous requests and content. | Includes text, images, audio, strokes, and administrative changes. | System Tutor, Administrator | Dynamic |
| cap-SEC-0004 | Inspect uploaded content safely | Detect unsupported, oversized, malformed, or harmful files before use. | Rejection must allow lesson recovery. | Student, System Tutor, Administrator | Dynamic |
| cap-SEC-0005 | Isolate private learner evidence | Prevent one student or unrelated actor from accessing another's submissions. | Content access does not imply evidence access. | Student, System Tutor, Administrator | Dynamic |
| cap-SEC-0006 | Restrict evidence action by ability | Separately authorize viewing, assessing, storing, exporting, and deleting evidence. | Fine-grained ability scopes may name a specific learner. | Student, System Tutor, Administrator | Dynamic |
| cap-SEC-0007 | Restrict content-management action by ability | Separately authorize creating, editing, reviewing, approving, publishing, withdrawing, and pricing content. | No persona automatically receives these abilities. | System Tutor, Administrator | Dynamic |
| cap-SEC-0008 | Detect suspicious activity | Identify unusual sign-in, request, purchase, evidence, or administration behavior. | Enables challenge, limitation, or investigation. | System Tutor, Administrator | Dynamic |
| cap-SEC-0009 | Limit abusive requests | Reduce excessive or automated misuse. | Must avoid unnecessarily blocking legitimate learning. | System Tutor, Administrator | Dynamic |
| cap-SEC-0010 | Fail closed on unknown authorization | Do not perform a protected action when permission cannot be established. | Lesson recovery may offer an unprotected alternative. | System Tutor | Dynamic |
| cap-SEC-0011 | Protect security credentials | Keep product credentials secret and replace them when compromised. | Applies to operational integrations and environments. | System Tutor, Administrator | Dynamic |
| cap-SEC-0012 | Separate test and real activity | Prevent test payments, content, learner data, or synthetic-agent sessions from affecting real access or learner outcomes. | Supports safe development and pilot operations; synthetic sessions remain identifiable and excluded from pupil evidence and measures. | Automated Agent, System Tutor, Administrator | Dynamic |
| cap-SEC-0013 | Record security audit | Preserve important authentication, ability, evidence, purchase, refund, publication, deletion, and configuration events. | Avoids unnecessary sensitive content in the audit. | System Tutor, Administrator | Dynamic |
| cap-SEC-0014 | Explain authorization decision | State why access was granted or refused at an appropriate level. | Does not disclose protected data or exploitable internals. | Student, Administrator | Dynamic |
| cap-SEC-0015 | Recover from security incident | Contain impact, revoke compromised access, restore trusted state, notify appropriately, and review causes. | Covers accounts, entitlements, progress, content, and evidence. | System Tutor, Administrator | Dynamic |
| cap-SEC-0016 | Correct entitlement integrity | Restore the intended ability collection after error or malicious change. | Verifies purchases and preserves unrelated abilities. | System Tutor, Administrator | Dynamic |
| cap-SEC-0017 | Secure content publication | **Composite:** authorize, review, approve, publish, audit, and support withdrawal or restoration. | Prevents unreviewed changes from silently altering live lessons. | System Tutor, Administrator | Dynamic |

## 21. Child and guardian safety

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-CHD-0001 | Determine guardian involvement | Identify when consent or management by an authorized adult is required. | Depends on audience, jurisdiction, and product policy to be defined later. | Student, System Tutor | Dynamic |
| cap-CHD-0002 | Obtain guardian authorization | Record appropriate approval for a child learner's participation or action. | Authorization is expressed through explicit abilities, not a guardian role. | Student, System Tutor | Dynamic |
| cap-CHD-0003 | Restrict child purchase | Require an explicitly authorized path for applicable purchases. | Prevents persona labels from acting as blanket permission. | Student, System Tutor | Dynamic |
| cap-CHD-0004 | Minimize child data | Collect and retain less information for younger learners where appropriate. | Includes age-appropriate evidence and retention choices. | System Tutor, Administrator | Dynamic |
| cap-CHD-0005 | Present age-appropriate privacy explanation | Explain collection, consent, and deletion understandably. | Presentation varies without changing core Telugu objectives. | Student, System Tutor | Static |
| cap-CHD-0006 | Apply child-appropriate content access | Prevent unsuitable content from being assigned or presented. | Governed by explicit content abilities and suitability information. | Student, System Tutor, Administrator | Dynamic |

## 22. Core authorization principle

The authorization model is:

```text
Actor
  -> collection of explicitly granted abilities
       -> content-access abilities
       -> costly tutor-operation abilities
       -> learner-evidence abilities
       -> content-management abilities
       -> commerce and security abilities
```

Educational readiness and commercial entitlement remain independent:

```text
Authentication: Who is making the request?
Ability authorization: Is this actor explicitly allowed to perform this action?
Content entitlement: May this student use this learning resource?
Educational eligibility: Is this the appropriate learning resource to study next?
Purchase: How can the required abilities be acquired?
```

Owning a chapter does not demonstrate mastery of its prerequisites. Completing a prerequisite does not imply that paid content has been purchased. Content access does not imply access to learner evidence, and access to evidence does not imply permission to modify progress or content.

## 23. Course orientation and structure

| Canonical ID | Name | Definition | Description | Example personas involved | Computation mode |
|---|---|---|---|---|---|
| cap-CRS-0001 | Present course approach and contents | Explain how the course teaches and show what the course contains. | Includes the practical course outcome, learning approach, sequence, table of contents, expected learning modes, and the relationship among courses, chapters, lessons, and reusable units. The presentation reflects an approved course version and does not assess the student. | Student, System Tutor | Static |

## Appendix A. Personas

The persona column gives examples of people or agents involved in a capability as an invoker, operator, configurator, subject, or direct beneficiary. It does not mean that every listed persona can perform every action named in the row. Personas are **not authorization roles** and do not automatically confer access. Every actor receives an explicit collection of granted abilities; authorization is evaluated from those abilities.

| Persona | Definition |
|---|---|
| **Student** | The person learning Telugu, including an adult, teenager, or child where the experience is appropriate for them. |
| **Tutor** | A qualified human Telugu-language or language-pedagogy reviewer. The Tutor is required only for the human review capabilities identified below; routine lesson delivery and assessment belong to the System Tutor. |
| **System Tutor** | The software tutor that presents instruction, observes responses, adapts help, assesses evidence when reliable, and preserves progress. |
| **Automated Agent** | An AI or other software actor interacting with the tutor. It may be a trusted, explicitly identified test actor or an undeclared actor detected only with uncertainty; those cases must not be treated as equivalent for identity or authorization. |
| **Administrator** | A person or operational agent maintaining content, localization, commerce, security, support, or product configuration through explicitly granted abilities. |

## Appendix B. Capabilities requiring a human Tutor

Human Tutor involvement is intentionally minimized. The present specifications require a human only where language correctness, naturalness, cultural suitability, or instruction-language pronunciation guidance needs accountable expert judgment. Tools and the System Tutor may assist these reviews, but they do not replace the human decision.

| Capability | Why a human Tutor is needed |
|---|---|
| **Review localized content** | A person must judge whether meanings, explanations, terminology, feedback, cultural context, and pronunciation guidance are accurate, natural, and pedagogically suitable in the instruction language. |
| **Review transliteration variant** | A person familiar with Telugu and the instruction language must judge whether the chosen script, spelling conventions, syllable divisions, and sound approximations will guide learners correctly. |
| **Review canonical Telugu** | A qualified Telugu speaker must confirm that canonical text, usage, explanations, pronunciation, and recordings are correct and natural before pupil testing or publication. |

No other capability in this catalogue requires a human Tutor. A human may participate elsewhere if explicitly granted the relevant ability, but that is optional involvement rather than a product dependency.

## Appendix C. How to read the capability tables

- **Canonical ID** is the immutable `cap-XXX-YYYY` identifier used to refer to the capability across specifications and future functional requirements.
- **Name** is the current conceptual name of the capability, not a proposed code symbol; it may be clarified without changing the canonical ID.
- **Definition** states the outcome the capability makes possible.
- **Description** clarifies its intended scope without prescribing an implementation.
- **Example personas involved** identifies likely participants or beneficiaries. It is illustrative and does not grant authorization.
- **Computation mode** indicates whether the capability outcome is Static, Dynamic, or Hybrid under the definitions near the beginning of this document.
- **Composite** in a definition means the capability coordinates several smaller capabilities.

## Appendix D. Computation modes

The computation mode describes how the **outcome of a capability** is obtained and whether that outcome can be reused. It does not describe when a screen is displayed or when a stored item is read. A static recording can be played during a live lesson; playing it at runtime does not make the instructional recording dynamic.

### Static

A Static capability produces or supplies an outcome that is prepared during course or product design and can be reused unchanged for multiple students and sessions.

Static outcomes remain valid until an identified dependency changes, such as:

- the course or lesson version;
- canonical Telugu content;
- an instruction-language variant;
- a reviewed recording, image, illustration, animation, or interface asset;
- a content-access classification; or
- the approval or review status of the material.

Examples include localized instructions, lesson missions, model audio, character explanations, dialogue scenes, instructional images, reviewed transliteration variants, and canonical character or grammar units.

A Static outcome may be stored, distributed, cached, or loaded during a lesson. It does not need to be regenerated merely because a different student requests it. When its source version changes, the Static outcome must be invalidated, reviewed, or replaced as appropriate.

### Dynamic

A Dynamic capability must produce, retrieve, record, or verify its outcome for the current actor, student, request, response, session, device state, transaction, or point in time.

Dynamic outcomes include:

- learner speech, writing, answers, reflections, and other responses;
- assessment results and confidence in those assessments;
- objective evidence, progress, retries, prompts used, and completion state;
- consent decisions and access to sensitive evidence;
- authentication, authorization, entitlement, and allowance decisions;
- purchases, refunds, subscriptions, and current prices or eligibility;
- microphone, camera, recording, playback, and processing state; and
- security, abuse, automated-agent, and incident decisions.

Dynamic information may be stored or temporarily cached for operational reasons, but a previous result must not be treated as current when the relevant actor, request, resource, state, or time may have changed.

Security material illustrates this distinction: credentials, public keys, and authorization policy may be cached securely, but authentication and authorization decisions remain Dynamic. The product must verify the applicable current material and state for the protected action rather than reusing an earlier allow decision.

Learner information follows the same rule. A prior response may be stored, but retrieving the correct response, confirming access to it, recording a new response, and updating evidence or progress are Dynamic capabilities.

### Hybrid

A Hybrid capability combines one or more Static outcomes with Dynamic state or computation.

Typical Hybrid behavior is:

1. obtain reusable course material, templates, or localized assets;
2. inspect the current student, lesson, instruction language, progress, entitlement, device, or response state; and
3. select, arrange, personalize, or present the appropriate material for that interaction.

Examples include selecting the correct localized asset, producing response-specific feedback from approved terminology, conducting a full lesson from static content and live learner evidence, presenting a catalogue containing both static descriptions and current ownership, and routing a suspected automated agent to a configured tutorial experience.

Only the Static portion of a Hybrid capability may be reused without reevaluating current state. The Dynamic portion must run again whenever its relevant inputs may have changed.

### Classification test

Use these questions in order when classifying a new capability:

1. **Does its outcome depend on the current learner, response, session, request, transaction, authorization, device, or time?** If yes, classify it as Dynamic unless it also materially composes reusable instructional material.
2. **Can the same approved outcome be reused unchanged for different learners until a content or configuration version changes?** If yes, classify it as Static.
3. **Does it combine reusable material with current state to select, compose, personalize, or route an experience?** If yes, classify it as Hybrid.
4. **Would reusing yesterday's decision create a security, privacy, payment, consent, or learning-evidence error?** If yes, the decision-making part is Dynamic.

When uncertain, classify the capability as Dynamic until its reusable Static portion is identified explicitly. This avoids treating learner-specific or security-sensitive state as durable course content.
