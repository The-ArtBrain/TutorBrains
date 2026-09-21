"""Check real page generation and failures that must not replace published output."""

from html.parser import HTMLParser
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

BUILD_TOOLS_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BUILD_TOOLS_ROOT))

from stages.course_content import generate_course_content
from stages.include_html import include_html_files
from stages.merge_instructions import merge_html_and_instructions
from stages.page_instructions import read_yaml_values
from stages.publish import publish_static_site

REPOSITORY_ROOT = BUILD_TOOLS_ROOT.parents[2]


class Document(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.elements = []
        self.text = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


class PageLocalizationTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.app = self.root / "apps/learner-web"
        self.content = self.root / "content"
        self.app.mkdir(parents=True)
        for name in ("html", "css", "assets"):
            shutil.copytree(REPOSITORY_ROOT / "apps/learner-web" / name, self.app / name)
        shutil.copytree(REPOSITORY_ROOT / "content", self.content)
        self.build_count = 0

    def build_language(self, language):
        self.build_count += 1
        work = self.root / f"work-{self.build_count}"
        included_html_root = work / "included-html"
        include_html_files(
            source_html_root=self.app / "html",
            destination_html_root=included_html_root,
        )
        lessons = merge_html_and_instructions(
            source_html_root=included_html_root,
            work_root=work,
            course_root=self.content / "subjects/languages/te/courses/practical-telugu",
            page_content_root=self.content,
            instruction_language=language,
        )
        generate_course_content(lessons=lessons)
        publish_static_site(
            learner_web_root=self.app,
            prepared_html_root=work / "html",
            instruction_language=language,
        )
        return self.app / "dist" / language / "html/pages"

    def test_all_pages_generate_in_both_languages_with_valid_links_and_semantics(self):
        expected_titles = {
            "en": ["Welcome", "Chapter 01", "Preferences", "Sign in", "Card pattern catalogue"],
            "hi": ["स्वागत", "अध्याय 01", "प्राथमिकताएँ", "साइन इन करें", "कार्ड नमूना सूची"],
        }
        names = ["index", "chapter-01", "preferences", "sign-in", "patterns"]
        for language in ("en", "hi"):
            self.build_language(language)
        for language in ("en", "hi"):
            pages = self.app / "dist" / language / "html/pages"
            self.assertEqual(len(list(pages.glob("*.html"))), 6)
            self.assertFalse((pages / "chapter.html").exists())
            self.assertFalse((pages / "lesson.html").exists())
            for name, title in zip(names, expected_titles[language]):
                html = (pages / f"{name}.html").read_text()
                with self.subTest(language=language, page=name):
                    self.assertIn(f"<title>{title} ·", html)
            for page in pages.glob("*.html"):
                html = page.read_text()
                with self.subTest(language=language, page=page.name):
                    self.assertNotIn("[#", html)
                    self.assertNotIn("data-placeholder", html)
                    doc = Document(html)
                    self.assertIn(("html", {"lang": f"{language}-IN"}), doc.elements)
                    ids = [attrs["id"] for _, attrs in doc.elements if "id" in attrs]
                    self.assertEqual(len(ids), len(set(ids)))
                    for tag, attrs in doc.elements:
                        self.assertNotEqual(tag, "script")
                        self.assertFalse(any(key.startswith("on") for key in attrs))
                        for attribute in ("aria-labelledby", "aria-describedby"):
                            for ref in attrs.get(attribute, "").split():
                                self.assertIn(ref, ids)
                        if tag == "label":
                            self.assertIn(attrs["for"], ids)
                        for attribute in ("href", "src"):
                            link = attrs.get(attribute, "")
                            if link and not link.startswith("#"):
                                self.assertTrue((page.parent / link).is_file(), link)
                        if tag == "option" and "selected" in attrs and "lang" in attrs:
                            self.assertEqual(attrs["lang"], language)
            self.assertIn("నమస్కారం. బాగున్నారా?", (pages / "chapter-01.html").read_text())
            catalogue = (pages / "patterns.html").read_text()
            self.assertIn('lang="en-IN"', catalogue)
            self.assertIn('lang="hi-IN"', catalogue)
            self.assertIn("English instruction-language specimen", catalogue)
            self.assertIn("हिन्दी निर्देश-भाषा नमूना", catalogue)

    def test_yaml_changes_update_text_and_attributes_without_injecting_html(self):
        path = self.content / "index.en.yml"
        text = 'A "quoted" label <script>alert(1)</script> & more'
        source = path.read_text()
        import json
        import re
        for key in ("index-heading", "index-brand-home-label", "index-document-description"):
            source = re.sub(rf"^{key}:.*$", lambda _: f"{key}: {json.dumps(text)}", source, flags=re.MULTILINE)
        path.write_text(source)
        pages = self.build_language("en")
        doc = Document((pages / "index.html").read_text())
        self.assertIn(text, doc.text)
        self.assertIn(text, [attrs.get("aria-label") for _, attrs in doc.elements])
        self.assertIn(text, [attrs.get("content") for tag, attrs in doc.elements if tag == "meta"])
        self.assertNotIn("script", [tag for tag, _ in doc.elements])

    def test_account_menu_include_updates_every_generated_page(self):
        partial = self.app / "html/includes/account-menu.inc"
        partial.write_text(partial.read_text().replace(
            'class="account-menu"', 'class="account-menu" data-shared-menu="yes"'
        ))

        pages = self.build_language("en")
        for page in pages.glob("*.html"):
            with self.subTest(page=page.name):
                html = page.read_text()
                self.assertEqual(html.count('data-shared-menu="yes"'), 1)
                self.assertNotIn("#include file=", html)
        self.assertFalse(list((self.app / "dist/en/html/includes").glob("*.inc")))

    def test_chapter_and_lesson_outputs_use_their_own_content_folders(self):
        course = self.content / "subjects/languages/te/courses/practical-telugu"
        first_chapter = course / "chapter-01"
        second_chapter = course / "chapter-02"
        shutil.copytree(first_chapter, second_chapter)
        (second_chapter / "chapter.en.yml").write_text(
            (second_chapter / "chapter.en.yml").read_text().replace("Chapter 01", "Chapter 02").replace(
                'chapter-heading: "Greet someone respectfully"',
                'chapter-heading: "Second chapter only"',
            ),
            encoding="utf-8",
        )
        (second_chapter / "chapter.yml").write_text(
            (second_chapter / "chapter.yml").read_text().replace("నమస్కారం. బాగున్నారా?", "రెండవ అధ్యాయం"),
            encoding="utf-8",
        )
        (second_chapter / "lesson-01/lesson.en.txt").write_text(
            (second_chapter / "lesson-01/lesson.en.txt").read_text().replace(
                "Lesson 1 · Greeting exchange · Telugu Tutor", "Second chapter lesson"
            ),
            encoding="utf-8",
        )
        second_lesson = first_chapter / "lesson-02"
        shutil.copytree(first_chapter / "lesson-01", second_lesson)
        (second_lesson / "lesson.en.txt").write_text(
            (second_lesson / "lesson.en.txt").read_text().replace(
                "Lesson 1 · Greeting exchange · Telugu Tutor", "First chapter second lesson"
            ),
            encoding="utf-8",
        )
        (second_lesson / "overview.en.yml").write_text(
            (second_lesson / "overview.en.yml").read_text().replace(
                'lesson-title: "Greet someone"', 'lesson-title: "Second listed lesson"'
            ),
            encoding="utf-8",
        )

        pages = self.build_language("en")
        self.assertEqual(len(list(pages.glob("*.html"))), 9)
        self.assertIn("Greet someone respectfully", (pages / "chapter-01.html").read_text())
        self.assertNotIn("Second chapter only", (pages / "chapter-01.html").read_text())
        self.assertIn("Second chapter only", (pages / "chapter-02.html").read_text())
        self.assertIn("<title>Chapter 02", (pages / "chapter-02.html").read_text())
        self.assertIn("రెండవ అధ్యాయం", (pages / "chapter-02.html").read_text())
        self.assertIn("First chapter second lesson", (pages / "chapter-01-lesson-02.html").read_text())
        self.assertIn("Second listed lesson", (pages / "chapter-01.html").read_text())
        self.assertIn('href="chapter-01-lesson-02.html"', (pages / "chapter-01.html").read_text())
        self.assertIn("Second chapter lesson", (pages / "chapter-02-lesson-01.html").read_text())
        self.assertIn('href="chapter-02.html"', (pages / "chapter-02-lesson-01.html").read_text())
        self.assertIn('href="chapter-02-lesson-01.html"', (pages / "chapter-02.html").read_text())

    def test_incomplete_translations_do_not_replace_previous_publication(self):
        pages = self.build_language("hi")
        before = {p.name: p.read_bytes() for p in pages.glob("*.html")}
        path = self.content / "preferences.hi.yml"
        original = path.read_text()
        path.unlink()
        with self.assertRaisesRegex(FileNotFoundError, "preferences.hi.yml"):
            self.build_language("hi")
        path.write_text("\n".join(line for line in original.splitlines() if not line.startswith("preferences-save-label:")))
        with self.assertRaisesRegex(ValueError, "Unresolved HTML placeholders.*preferences-save-label"):
            self.build_language("hi")
        path.write_text(original + '\npreferences-typo: "Unused"\n')
        with self.assertRaisesRegex(ValueError, "preferences-typo.*not used"):
            self.build_language("hi")
        self.assertEqual(before, {p.name: p.read_bytes() for p in pages.glob("*.html")})

    def test_yaml_validation_and_multiline_text(self):
        path = self.content / "example.en.yml"
        path.write_text('label: |-\n  First line\n  Second line\n')
        self.assertEqual(read_yaml_values(path), {"label": "First line\nSecond line"})
        for invalid in (
            'label: One\nlabel: Two\n',
            'label: 123\n',
            'label: true\n',
            'label: ""\n',
            'label: [one, two]\n',
            'label: {nested: value}\n',
            'bad_key: value\n',
            'label: "[#another-label]"\n',
            'label: !!python/object:example {}\n',
        ):
            with self.subTest(invalid=invalid):
                path.write_text(invalid)
                with self.assertRaisesRegex(ValueError, "example.en.yml"):
                    read_yaml_values(path)

    def test_publication_rejects_unprocessed_pages(self):
        pages = self.build_language("en")
        before = (pages / "index.html").read_bytes()
        with self.assertRaisesRegex(ValueError, "Unresolved HTML placeholders"):
            publish_static_site(
                learner_web_root=self.app,
                prepared_html_root=self.app / "html",
                instruction_language="en",
            )
        self.assertEqual(before, (pages / "index.html").read_bytes())


if __name__ == "__main__":
    unittest.main()
