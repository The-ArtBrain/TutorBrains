"""Unit tests for the learner-web build pipeline."""

from pathlib import Path
import sys
import tempfile
import unittest


BUILD_TOOLS_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BUILD_TOOLS_ROOT))

import build  # noqa: E402
from stages.course_content import generate_course_content  # noqa: E402
from stages.include_html import include_html_files  # noqa: E402
from stages.merge_instructions import (  # noqa: E402
    merge_html_and_instructions,
    merge_values,
    read_values,
)
from stages.publish import publish_static_site  # noqa: E402


class BuildParameterTests(unittest.TestCase):
    def test_defaults_select_english_practical_telugu(self) -> None:
        options = build.parse_arguments([])

        self.assertEqual(options.instruction_language, "en")
        self.assertEqual(options.course_name, "telugu")
        self.assertEqual(options.course_content_folder, "practical telugu")
        self.assertEqual(options.distribution_root, "telugu")
        self.assertEqual(options.command, "build")

    def test_clean_command_is_selected_explicitly(self) -> None:
        options = build.parse_arguments(["clean"])

        self.assertEqual(options.command, "clean")

    def test_course_names_resolve_to_repository_folders(self) -> None:
        root = Path("/repository")

        course_root = build.resolve_course_root(
            repository_root=root,
            course_name="Telugu",
            course_content_folder="Practical Telugu",
        )

        self.assertEqual(
            course_root,
            root / "content/subjects/languages/te/courses/practical-telugu",
        )

    def test_explicit_parameters_override_defaults(self) -> None:
        options = build.parse_arguments(
            [
                "--instruction-language",
                "hi",
                "--course-name",
                "telugu",
                "--course-content-folder",
                "another course",
                "--distribution-root",
                "another-root",
            ]
        )

        self.assertEqual(options.instruction_language, "hi")
        self.assertEqual(options.course_name, "telugu")
        self.assertEqual(options.course_content_folder, "another course")
        self.assertEqual(options.distribution_root, "another-root")


class ContentFileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_reads_identifier_blocks_and_multiline_values(self) -> None:
        source = self.root / "values.txt"
        source.write_text("[first]\nLine one\nLine two\n\n[second]\nValue two\n", encoding="utf-8")

        self.assertEqual(
            read_values(source),
            {"first": "Line one\nLine two", "second": "Value two"},
        )

    def test_rejects_conflicting_values(self) -> None:
        with self.assertRaisesRegex(ValueError, "Conflicting value"):
            merge_values(
                (Path("one.txt"), {"shared": "One"}),
                (Path("two.txt"), {"shared": "Two"}),
            )


class IncludeStageTests(unittest.TestCase):
    def test_includes_the_named_file_before_other_build_stages(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            (source / "pages").mkdir(parents=True)
            (source / "includes").mkdir()
            (source / "includes/navigation.inc").write_text("<nav>Links</nav>\n", encoding="utf-8")
            (source / "pages/example.html").write_text(
                '<header>\n  <!--#include file="../includes/navigation.inc" -->\n</header>\n',
                encoding="utf-8",
            )

            include_html_files(source_html_root=source, destination_html_root=root / "included")

            self.assertEqual(
                (root / "included/pages/example.html").read_text(encoding="utf-8"),
                "<header>\n  <nav>Links</nav>\n</header>\n",
            )

    def test_rejects_an_include_inside_an_included_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            (source / "pages").mkdir(parents=True)
            (source / "includes").mkdir()
            (source / "pages/example.html").write_text(
                '<!--#include file="../includes/outer.inc" -->\n', encoding="utf-8"
            )
            (source / "includes/outer.inc").write_text(
                '<!--#include file="inner.inc" -->\n', encoding="utf-8"
            )
            (source / "includes/inner.inc").write_text("<nav>Links</nav>\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Nested HTML include.*outer.inc"):
                include_html_files(source_html_root=source, destination_html_root=root / "included")


class BuildStageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.learner_web_root = self.root / "apps/learner-web"
        self.source_html_root = self.learner_web_root / "html"
        self.pages_root = self.source_html_root / "pages"
        self.course_root = self.root / "content/subjects/languages/te/courses/practical-telugu"
        self.lesson_root = self.course_root / "chapter-01/lesson-01"

        self.pages_root.mkdir(parents=True)
        (self.learner_web_root / "css").mkdir(parents=True)
        (self.learner_web_root / "assets").mkdir(parents=True)
        self.lesson_root.mkdir(parents=True)

        (self.learner_web_root / "css/site.css").write_text("body {}\n", encoding="utf-8")
        (self.learner_web_root / "assets/icon.svg").write_text("<svg></svg>\n", encoding="utf-8")
        (self.learner_web_root / "index.html").write_text(
            '<meta http-equiv="refresh" content="0; url=en/index.html">',
            encoding="utf-8",
        )
        (self.learner_web_root / "assets/.DS_Store").write_text("ignored", encoding="utf-8")
        (self.course_root / "cards.en.txt").write_text(
            "[instruction-language-tag]\nen-IN\n\n"
            "[instruction-label]\nFollow the instruction.\n",
            encoding="utf-8",
        )
        (self.lesson_root / "lesson.en.txt").write_text(
            "[lesson-title]\nGreeting lesson\n",
            encoding="utf-8",
        )
        (self.lesson_root / "lesson.txt").write_text(
            "[target-expression]\nనమస్కారం\n",
            encoding="utf-8",
        )
        (self.lesson_root / "overview.en.yml").write_text('lesson-title: "Greeting lesson"\n', encoding="utf-8")
        (self.lesson_root.parent / "chapter.yml").write_text('chapter-greeting: "నమస్కారం"\n', encoding="utf-8")
        (self.lesson_root.parent / "chapter.en.yml").write_text('chapter-heading: "Greeting chapter"\n', encoding="utf-8")
        (self.pages_root / "chapter.html").write_text(
            '<html lang="[#instruction-language-tag]"><head></head><body>'
            '<h1>[#chapter-heading]</h1><p>[#chapter-greeting]</p>'
            '<!-- lesson-list:start --><article aria-labelledby="lesson-title">'
            '<h2 id="lesson-title">[#lesson-title]</h2><a href="lesson.html">Start lesson</a>'
            '</article><!-- lesson-list:end --></body></html>',
            encoding="utf-8",
        )
        (self.pages_root / "lesson.html").write_text(
            """<!doctype html>
<html lang="en-IN"><body>
<link rel="alternate" hreflang="en" href="lesson-01.html">
<link rel="alternate" hreflang="hi" href="lesson-01.html">
<data id="instruction-label">old instruction</data>
<data id="lesson-title">old title</data>
<data id="target-expression" lang="te">old target</data>
<h1><span class="heading data-placeholder" data-source="#lesson-title">[#lesson-title]</span></h1>
<p><span class="data-placeholder" data-source="#instruction-label">[#instruction-label]</span></p>
<p><span class="target data-placeholder" data-source="#target-expression">[#target-expression]</span></p>
</body></html>
""",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_clean_removes_only_generated_distribution(self) -> None:
        source_file = self.pages_root / "lesson.html"
        generated_file = self.learner_web_root / "dist/telugu/en/chapter-01-lesson-01.html"
        generated_file.parent.mkdir(parents=True)
        generated_file.write_text("generated", encoding="utf-8")

        removed = build.clean_distribution(learner_web_root=self.learner_web_root)

        self.assertTrue(removed)
        self.assertFalse((self.learner_web_root / "dist").exists())
        self.assertTrue(source_file.is_file())
        self.assertFalse(build.clean_distribution(learner_web_root=self.learner_web_root))

    def test_three_stages_merge_generate_and_publish(self) -> None:
        work_root = self.root / "work"

        lessons = merge_html_and_instructions(
            source_html_root=self.source_html_root,
            work_root=work_root,
            course_root=self.course_root,
            page_content_root=self.root / "content",
            instruction_language="en",
        )
        after_instructions = lessons[0].html_path.read_text(encoding="utf-8")
        self.assertIn("Greeting lesson", after_instructions)
        self.assertIn("Follow the instruction.", after_instructions)
        self.assertIn("[#target-expression]", after_instructions)

        generated = generate_course_content(lessons=lessons)
        final_html = generated[0].read_text(encoding="utf-8")
        self.assertIn("నమస్కారం", final_html)
        self.assertNotIn("data-placeholder", final_html)
        self.assertNotIn("data-source", final_html)
        self.assertNotIn("[#", final_html)
        self.assertIn('class="heading"', final_html)

        (self.learner_web_root / "dist/telugu/en").mkdir(parents=True)
        (self.learner_web_root / "dist/telugu/en/stale.txt").write_text("stale", encoding="utf-8")
        published_files = publish_static_site(
            learner_web_root=self.learner_web_root,
            prepared_html_root=work_root / "html",
            instruction_language="en",
        )

        self.assertEqual(published_files, 5)
        self.assertTrue((self.learner_web_root / "dist/telugu/index.html").is_file())
        self.assertEqual(
            (self.learner_web_root / "dist/telugu/en/chapter-01-lesson-01.html").read_text(encoding="utf-8"),
            final_html,
        )
        self.assertIn("Greeting chapter", (self.learner_web_root / "dist/telugu/en/chapter-01.html").read_text())
        self.assertTrue((self.learner_web_root / "dist/telugu/en/css/site.css").is_file())
        self.assertTrue((self.learner_web_root / "dist/telugu/en/assets/icon.svg").is_file())
        self.assertFalse((self.learner_web_root / "dist/telugu/en/assets/.DS_Store").exists())
        self.assertFalse((self.learner_web_root / "dist/telugu/en/stale.txt").exists())

    def test_hindi_build_uses_same_lesson_template_and_preserves_english_output(self) -> None:
        (self.course_root / "cards.hi.txt").write_text(
            "[instruction-language-tag]\nhi-IN\n\n"
            "[instruction-label]\nनिर्देश का पालन करें।\n",
            encoding="utf-8",
        )
        (self.lesson_root / "lesson.hi.txt").write_text(
            "[lesson-title]\nअभिवादन पाठ\n",
            encoding="utf-8",
        )
        (self.lesson_root / "overview.hi.yml").write_text('lesson-title: "अभिवादन पाठ"\n', encoding="utf-8")
        (self.lesson_root.parent / "chapter.hi.yml").write_text('chapter-heading: "अभिवादन अध्याय"\n', encoding="utf-8")
        english_output = self.learner_web_root / "dist/telugu/en/keep.txt"
        english_output.parent.mkdir(parents=True)
        english_output.write_text("keep", encoding="utf-8")

        work_root = self.root / "work-hi"
        lessons = merge_html_and_instructions(
            source_html_root=self.source_html_root,
            work_root=work_root,
            course_root=self.course_root,
            page_content_root=self.root / "content",
            instruction_language="hi",
        )
        generate_course_content(lessons=lessons)
        publish_static_site(
            learner_web_root=self.learner_web_root,
            prepared_html_root=work_root / "html",
            instruction_language="hi",
        )

        hindi_html = (self.learner_web_root / "dist/telugu/hi/chapter-01-lesson-01.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("अभिवादन पाठ", hindi_html)
        self.assertIn("निर्देश का पालन करें।", hindi_html)
        self.assertIn("నమస్కారం", hindi_html)
        self.assertIn('<html lang="hi-IN">', hindi_html)
        self.assertIn(
            '<link rel="alternate" hreflang="en" href="../en/chapter-01-lesson-01.html">',
            hindi_html,
        )
        self.assertNotIn("lesson-01-hi.html", hindi_html)
        self.assertTrue(english_output.is_file())
        self.assertFalse((self.pages_root / "lesson-01-hi.html").exists())
        self.assertIn("अभिवादन अध्याय", (self.learner_web_root / "dist/telugu/hi/chapter-01.html").read_text())

    def test_alternate_metadata_matches_generated_documents(self) -> None:
        (self.course_root / "cards.hi.txt").write_text(
            "[instruction-language-tag]\nhi-IN\n\n"
            "[instruction-label]\nनिर्देश का पालन करें।\n",
            encoding="utf-8",
        )
        (self.lesson_root / "lesson.hi.txt").write_text(
            "[lesson-title]\nअभिवादन पाठ\n",
            encoding="utf-8",
        )
        (self.lesson_root / "overview.hi.yml").write_text('lesson-title: "अभिवादन पाठ"\n', encoding="utf-8")
        (self.lesson_root.parent / "chapter.hi.yml").write_text('chapter-heading: "अभिवादन अध्याय"\n', encoding="utf-8")

        for language in ("en", "hi"):
            with self.subTest(language=language):
                lessons = merge_html_and_instructions(
                    source_html_root=self.source_html_root,
                    work_root=self.root / f"work-{language}",
                    course_root=self.course_root,
                    page_content_root=self.root / "content",
                    instruction_language=language,
                )
                html = lessons[0].html_path.read_text(encoding="utf-8")

                for available_language in ("en", "hi"):
                    self.assertIn(
                        f'<link rel="alternate" hreflang="{available_language}" '
                        f'href="../{available_language}/chapter-01-lesson-01.html">',
                        html,
                    )

    def test_missing_language_file_stops_before_publication(self) -> None:
        with self.assertRaisesRegex(FileNotFoundError, "cards.hi.txt"):
            merge_html_and_instructions(
                source_html_root=self.source_html_root,
                work_root=self.root / "work",
                course_root=self.course_root,
                page_content_root=self.root / "content",
                instruction_language="hi",
            )

        self.assertFalse((self.learner_web_root / "dist").exists())


if __name__ == "__main__":
    unittest.main()
