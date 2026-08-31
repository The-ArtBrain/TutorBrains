# Learner Web agent guidance

## Scope

The current learner-web slice is a static semantic Hypertext Markup Language (HTML) and Cascading Style Sheets (CSS) prototype for review. Do not add JavaScript, a server, authentication integration, persistence, a content schema, or a data contract unless the issue explicitly expands the scope.

## HTML constraints

- Use native elements according to meaning before adding generic containers or custom behavior.
- Express Course → Chapter → Lesson through headings, sections, lists, navigation, and ordinary links.
- Represent each Card as one flat `article`. Task, help, response, and feedback are sibling sections within that Card, not child Cards.
- Preserve semantic source order at every viewport width. Do not duplicate learner content for desktop and mobile.
- Associate every form control with a visible `label`. Use buttons for actions and links for navigation.
- Declare the document language on `html`; mark embedded Telugu with `lang="te"` and transliterated Telugu with `lang="te-Latn"`.
- Keep localized words and accessibility text in HTML. Never generate them with CSS pseudo-elements.
- Treat Chapter 01 text as review data only. Do not infer a JSON shape, binding syntax, or final schema from the markup.

## CSS constraints

- Keep design values in `tokens.css`, element defaults in `base.css`, and reusable interface rules in `components.css`.
- Prefer class selectors. Do not style by generated identifiers or encode Course, Chapter, Lesson, Card, ability, or progress meaning in CSS.
- Use responsive reflow, not device-specific copies of content.
- Do not place learner-facing words in `content` declarations.

## Template constraints

- HTML `template` elements are inert interface examples, not the authoritative Course/Card model.
- Nested templates are allowed only when their relationship is understandable from the source and does not imply nested domain Cards.
- Keep IDs inside inert examples documented as placeholders because cloning would require a future implementation to make them unique.

## Review checks

- Confirm that pages remain understandable with CSS unavailable.
- Check headings, landmarks, link purpose, language metadata, unique active-document IDs, and label/control associations.
- Reject scripts, inline event handlers, network calls, provider-specific fields, hidden authorization behavior, and accidental data contracts in this phase.
