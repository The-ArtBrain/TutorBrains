# Multilingual Sitemap and Search Discovery Guidance

**Status:** Proposed implementation guidance  
**Scope:** Search discovery for the generated learner course site  
**Application:** `apps/learner-web`  
**Related:** [Cloudflare Pages hosting and DNS specification](CLOUDFLARE_PAGES_HOSTING_SPEC.md), [learner-web build instructions](../../apps/learner-web/build-tools/README.md)

## 1. Purpose

This document defines how the learner-web build should expose stable English- and Hindi-instruction course pages to search engines. It covers canonical URLs, language alternates, `sitemap.xml`, `robots.txt`, URL changes, and production verification.

English and Hindi pages are localized versions of the same lesson, not interchangeable duplicate URLs. Each localized page should be independently indexable and should identify the other language version as an alternate.

## 2. Language model

The document language is the language used for navigation, explanations, instructions, titles, and descriptions. It is not necessarily the language being taught.

| Page content | Language identifier |
|---|---|
| English instructions for learning Telugu | `en-IN` |
| Hindi instructions for learning Telugu | `hi-IN` |
| Telugu expression embedded in either page | `te` |
| Romanized Telugu embedded in either page | `te-Latn` |

An English instruction page therefore begins with:

```html
<html lang="en-IN">
```

A Hindi instruction page begins with:

```html
<html lang="hi-IN">
```

Embedded Telugu and transliteration retain their narrower language declarations:

```html
<span lang="te">నమస్కారం</span>
<span lang="te-Latn">Namaskāraṁ</span>
```

## 3. Stable URL policy

Every public page has one stable URL per instruction language. The route after the locale prefix should be identical for all translations.

Preferred long-term shape:

```text
https://learn.example.com/en/courses/practical-telugu/chapter-01/lesson-01/
https://learn.example.com/hi/courses/practical-telugu/chapter-01/lesson-01/
```

The production domain in this document is illustrative. The build must use the selected canonical production origin.

Stable routes should be derived from durable course, chapter, and lesson identifiers rather than translated titles. Changing display wording must not change a URL.

The current generated paths such as `/en/html/pages/chapter-01-lesson-01.html` may be used for the initial release if they are deliberately accepted as permanent public URLs. If clean URLs are wanted, introduce them before search indexing begins. A later change requires permanent redirects from every old URL.

URL rules:

- Use HTTPS URLs on the canonical custom domain.
- Use lowercase ASCII route identifiers.
- Select one trailing-slash policy and apply it consistently.
- Do not publish both `.html` and clean-path forms without redirecting one to the other.
- Do not use query parameters or fragments as page identities.
- Do not put translated titles into canonical path segments.
- Do not use the Cloudflare `pages.dev` hostname in production canonical metadata.

## 4. HTML metadata and sitemap responsibilities

These mechanisms have different purposes:

| Mechanism | Responsibility |
|---|---|
| `rel="canonical"` in HTML | Declares the preferred URL for that exact localized page |
| `rel="alternate" hreflang` in HTML | Connects translations of the same logical page |
| `sitemap.xml` | Helps search engines discover canonical public URLs |
| `robots.txt` | Provides crawler instructions and points to the sitemap |
| HTTP redirect | Permanently or temporarily moves a URL |

The sitemap does not replace canonical links. Canonical and alternate links should be present in the generated HTML source without depending on client-side JavaScript.

## 5. Page-level canonical and alternate links

Each page must canonicalize to itself in the same language.

For the English lesson:

```html
<link rel="canonical"
      href="https://learn.example.com/en/courses/practical-telugu/chapter-01/lesson-01/">
```

For the Hindi lesson:

```html
<link rel="canonical"
      href="https://learn.example.com/hi/courses/practical-telugu/chapter-01/lesson-01/">
```

Both pages must contain the same complete alternate set:

```html
<link rel="alternate" hreflang="en-IN"
      href="https://learn.example.com/en/courses/practical-telugu/chapter-01/lesson-01/">
<link rel="alternate" hreflang="hi-IN"
      href="https://learn.example.com/hi/courses/practical-telugu/chapter-01/lesson-01/">
<link rel="alternate" hreflang="x-default"
      href="https://learn.example.com/en/courses/practical-telugu/chapter-01/lesson-01/">
```

`x-default` initially points to English because English is the product fallback. It may instead point to a static language-selection page if one is introduced later.

Do not canonicalize a Hindi translation to its English counterpart. Doing so signals that the Hindi page is a duplicate and can prevent it from being selected independently for Hindi searches.

## 6. Sitemap contents

Publish one sitemap at:

```text
https://learn.example.com/sitemap.xml
```

Include:

- each canonical localized landing page;
- each canonical localized chapter page; and
- each canonical localized lesson page intended for public discovery.

Exclude:

- `/`, when it is only a temporary language redirect;
- sign-in, sign-out, callback, and account-management pages;
- pattern catalogues and staff-review fixtures;
- preview-deployment URLs;
- error pages;
- URL aliases and redirect sources;
- pages marked `noindex`; and
- URLs requiring authentication.

Only successful, public `200 OK` destinations belong in the sitemap.

## 7. Recommended initial sitemap format

Keep `hreflang` relationships in HTML and use the sitemap as a simple canonical URL inventory. This avoids maintaining the same relationship data in two output formats.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://learn.example.com/en/courses/practical-telugu/</loc>
  </url>
  <url>
    <loc>https://learn.example.com/hi/courses/practical-telugu/</loc>
  </url>
  <url>
    <loc>https://learn.example.com/en/courses/practical-telugu/chapter-01/lesson-01/</loc>
  </url>
  <url>
    <loc>https://learn.example.com/hi/courses/practical-telugu/chapter-01/lesson-01/</loc>
  </url>
</urlset>
```

Every special XML character in a URL must be escaped. The response must use an XML-compatible content type.

## 8. Optional sitemap-level language alternates

Google also supports expressing `hreflang` relationships in the sitemap. This is optional when the HTML already contains correct alternate links.

If sitemap-level alternates are adopted, every localized URL entry must repeat the complete set, including itself:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://learn.example.com/en/courses/practical-telugu/chapter-01/lesson-01/</loc>
    <xhtml:link rel="alternate" hreflang="en-IN"
      href="https://learn.example.com/en/courses/practical-telugu/chapter-01/lesson-01/"/>
    <xhtml:link rel="alternate" hreflang="hi-IN"
      href="https://learn.example.com/hi/courses/practical-telugu/chapter-01/lesson-01/"/>
    <xhtml:link rel="alternate" hreflang="x-default"
      href="https://learn.example.com/en/courses/practical-telugu/chapter-01/lesson-01/"/>
  </url>
  <url>
    <loc>https://learn.example.com/hi/courses/practical-telugu/chapter-01/lesson-01/</loc>
    <xhtml:link rel="alternate" hreflang="en-IN"
      href="https://learn.example.com/en/courses/practical-telugu/chapter-01/lesson-01/"/>
    <xhtml:link rel="alternate" hreflang="hi-IN"
      href="https://learn.example.com/hi/courses/practical-telugu/chapter-01/lesson-01/"/>
    <xhtml:link rel="alternate" hreflang="x-default"
      href="https://learn.example.com/en/courses/practical-telugu/chapter-01/lesson-01/"/>
  </url>
</urlset>
```

Do not manually maintain HTML and sitemap alternate mappings separately. Both must be generated from the same page identity and language mapping if this option is enabled.

## 9. `lastmod` policy

`<lastmod>` is optional. Include it only when the build can supply the date of a meaningful page-content change.

Valid example:

```xml
<lastmod>2026-09-24</lastmod>
```

Do not set every page to the deployment time on every build. Changes limited to infrastructure, unrelated files, or sitemap generation do not make all course pages newly modified.

Do not add `changefreq` or `priority`; they are unnecessary for this site and do not replace accurate discovery and internal linking.

## 10. `robots.txt`

Publish a static file at:

```text
https://learn.example.com/robots.txt
```

Initial production content:

```text
User-agent: *
Allow: /

Sitemap: https://learn.example.com/sitemap.xml
```

Do not use `robots.txt` to canonicalize pages or hide sensitive content. A URL blocked from crawling can still be discovered through links. Sensitive content must not be published as a public static asset.

## 11. Preview deployment policy

Cloudflare preview deployments must not compete with production pages in search results.

Preview responses should include:

```text
X-Robots-Tag: noindex, nofollow
```

Prefer deployment-level access protection when available. Preview pages must never declare a preview hostname as canonical. If production metadata is present in preview HTML for realistic testing, it must continue to point to the production custom domain.

Do not submit preview sitemaps to any search engine.

## 12. Build integration

The learner-web build should accept a canonical production origin, for example:

```text
https://learn.example.com
```

Production builds must fail when the origin is absent, malformed, non-HTTPS, contains a path, or uses a preview hostname.

From the discovered page and language records, the build should:

1. assign each logical page a stable route;
2. calculate its canonical URL;
3. calculate all available instruction-language alternates;
4. insert canonical and alternate links into the HTML `<head>`;
5. generate `dist/sitemap.xml`;
6. generate or copy `dist/robots.txt`; and
7. reject incomplete or asymmetric alternate mappings.

The build must not infer a Hindi page merely by replacing text inside an English URL. It should use the same chapter and lesson identifiers that generated both localized documents.

## 13. Validation requirements

Automated validation must verify:

- every sitemap URL is absolute and uses HTTPS;
- every sitemap URL uses the canonical production hostname;
- every sitemap URL resolves to a generated public page;
- no URL appears more than once;
- no sign-in, pattern, callback, preview, or redirect URL appears;
- every indexable HTML page has exactly one self-referencing canonical;
- every localized pair has reciprocal `hreflang` links;
- every alternate URL exists in the generated output;
- `hreflang`, `<html lang>`, and locale prefix agree;
- every `x-default` destination exists;
- the XML is well formed;
- `robots.txt` names the correct absolute sitemap URL; and
- no canonical or alternate URL uses `localhost` or `pages.dev`.

## 14. URL migrations

If a public URL changes after release:

1. add a permanent `301` or `308` redirect from the exact old URL to its corresponding new URL;
2. update internal links;
3. update the page canonical;
4. update all reciprocal alternates;
5. remove the old URL from the sitemap;
6. add the new URL to the sitemap; and
7. keep the redirect for at least one year and preferably indefinitely.

Do not redirect all retired lessons to the course home page. A removed page with no equivalent should return `404 Not Found` or `410 Gone`.

## 15. Search-engine setup

After the custom domain is live:

1. verify ownership of the canonical domain in Google Search Console;
2. submit `https://learn.example.com/sitemap.xml`;
3. inspect one English and one Hindi URL;
4. confirm the declared and Google-selected canonical URLs;
5. confirm that rendered HTML contains the reciprocal alternates;
6. request indexing for a small number of representative pages; and
7. monitor indexing, duplicate-page, canonical, and language-targeting reports after releases.

Search Console submission aids discovery but does not guarantee indexing or a particular ranking.

## 16. Acceptance criteria

This guidance is implemented when:

1. every public course page has a stable locale-prefixed URL;
2. English and Hindi pages canonicalize to themselves;
3. localized counterparts contain reciprocal absolute `hreflang` links;
4. `dist/sitemap.xml` lists every indexable canonical page exactly once;
5. `dist/robots.txt` points to the production sitemap;
6. non-course and non-indexable pages are excluded;
7. preview deployments are marked `noindex`;
8. automated tests reject missing, contradictory, or preview metadata; and
9. Google Search Console accepts the production sitemap without structural errors.

## 17. References

- [Google: Managing multilingual sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites)
- [Google: Localized versions of pages](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Google: Canonical URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Google: Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Sitemaps XML protocol](https://www.sitemaps.org/protocol.html)
