"""CLI regressions for visible text when resolving inline DOCX revisions."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from docx import Document
from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
HELPER = Path(os.environ.get("DOCUMENTS_HELPER_PATH", ROOT / "scripts/accept_tracked_changes.py"))
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}
SPACE = "{http://www.w3.org/XML/1998/namespace}space"
REVISION_TAGS = ("ins", "del", "moveTo", "moveFrom")


def word(tag: str) -> str:
    return f"{{{W_NS}}}{tag}"


def make_fixture(path: Path, content: str) -> None:
    """Use a real DOCX package, injecting only the controlled paragraph fixture."""
    doc = Document()
    doc.add_paragraph("FIXTURE_PARAGRAPH")
    doc.save(path)
    with zipfile.ZipFile(path) as z:
        parts = {name: z.read(name) for name in z.namelist()}
    document = etree.fromstring(parts["word/document.xml"])
    old = document.find(".//w:p", NS)
    old.getparent().replace(old, etree.fromstring(f'<w:p xmlns:w="{W_NS}">{content}</w:p>'))
    settings = etree.fromstring(parts["word/settings.xml"])
    etree.SubElement(settings, word("trackRevisions"))
    parts["word/document.xml"] = etree.tostring(document, xml_declaration=True, encoding="UTF-8", standalone=True)
    parts["word/settings.xml"] = etree.tostring(settings, xml_declaration=True, encoding="UTF-8", standalone=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, value in parts.items():
            z.writestr(name, value)


REPLACEMENT = (
    '<w:r><w:t xml:space="preserve">Before </w:t></w:r>'
    '<w:del w:id="1"><w:r><w:delText>original</w:delText></w:r></w:del>'
    '<w:ins w:id="2"><w:r><w:t>replacement</w:t></w:r></w:ins>'
    '<w:r><w:t xml:space="preserve"> after</w:t></w:r>'
)


class TrackedChangeCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory(prefix="revisions-", dir=os.environ.get("DOCUMENTS_TEST_TMPDIR"))
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.source = self.root / "source.docx"
        self.output = self.root / "output.docx"

    def run_helper(self, mode: str, *extra: str) -> subprocess.CompletedProcess[str]:
        args = [sys.executable, "-B", str(HELPER), str(self.source), "--mode", mode]
        if mode != "report":
            args.extend(["--out", str(self.output)])
        result = subprocess.run([*args, *extra], text=True, capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def document_xml(self) -> etree._Element:
        with zipfile.ZipFile(self.output) as z:
            self.assertIsNone(z.testzip())
            return etree.fromstring(z.read("word/document.xml"))

    def assert_clean(self, xml: etree._Element) -> None:
        for tag in (*REVISION_TAGS, "delText"):
            self.assertEqual(xml.findall(f".//w:{tag}", NS), [], tag)

    def visible_text(self) -> str:
        return "\n".join(paragraph.text for paragraph in Document(self.output).paragraphs)

    def test_reject_replacement_restores_original_visible_text(self) -> None:
        make_fixture(self.source, REPLACEMENT)
        before = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.run_helper("reject")
        self.assertEqual(self.visible_text(), "Before original after")
        self.assert_clean(self.document_xml())
        self.assertEqual(hashlib.sha256(self.source.read_bytes()).hexdigest(), before)

    def test_accept_replacement_keeps_inserted_visible_text(self) -> None:
        make_fixture(self.source, REPLACEMENT)
        self.run_helper("accept")
        self.assertEqual(self.visible_text(), "Before replacement after")
        self.assert_clean(self.document_xml())

    def test_reject_move_restores_source_text_and_drops_destination(self) -> None:
        make_fixture(self.source, (
            '<w:moveFrom w:id="1"><w:r><w:delText>moved</w:delText></w:r></w:moveFrom>'
            '<w:r><w:t xml:space="preserve"> between </w:t></w:r>'
            '<w:moveTo w:id="2"><w:r><w:t>moved</w:t></w:r></w:moveTo>'
        ))
        self.run_helper("reject")
        self.assertEqual(self.visible_text(), "moved between ")
        self.assert_clean(self.document_xml())

    def test_accept_move_keeps_destination_and_drops_source(self) -> None:
        make_fixture(self.source, (
            '<w:moveFrom w:id="1"><w:r><w:delText>moved</w:delText></w:r></w:moveFrom>'
            '<w:r><w:t xml:space="preserve"> between </w:t></w:r>'
            '<w:moveTo w:id="2"><w:r><w:t>moved</w:t></w:r></w:moveTo>'
        ))
        self.run_helper("accept")
        self.assertEqual(self.visible_text(), " between moved")
        self.assert_clean(self.document_xml())

    def test_reject_preserves_whitespace_run_formatting_and_control_characters(self) -> None:
        make_fixture(self.source, (
            '<w:del w:id="1"><w:r><w:rPr><w:b/></w:rPr>'
            '<w:delText xml:space="preserve">  old  </w:delText><w:tab/>'
            '<w:delText>second</w:delText><w:br/></w:r></w:del>'
        ))
        self.run_helper("reject")
        self.assertEqual(self.visible_text(), "  old  \tsecond\n")
        xml = self.document_xml()
        texts = xml.findall(".//w:t", NS)
        self.assertEqual(texts[0].get(SPACE), "preserve")
        self.assertEqual(len(xml.findall(".//w:rPr/w:b", NS)), 1)
        self.assert_clean(xml)

    def test_report_is_read_only_and_counts_revisions(self) -> None:
        make_fixture(self.source, REPLACEMENT)
        original = self.source.read_bytes()
        result = self.run_helper("report")
        self.assertIn("ins=1 del=1 moveTo=0 moveFrom=0", result.stdout)
        self.assertFalse(self.output.exists())
        self.assertEqual(self.source.read_bytes(), original)

    def test_only_document_and_tracking_settings_parts_change(self) -> None:
        make_fixture(self.source, REPLACEMENT)
        self.run_helper("reject")
        with zipfile.ZipFile(self.source) as source, zipfile.ZipFile(self.output) as output:
            self.assertEqual(set(source.namelist()), set(output.namelist()))
            for name in source.namelist():
                if name not in ("word/document.xml", "word/settings.xml"):
                    self.assertEqual(source.read(name), output.read(name), name)
            settings = etree.fromstring(output.read("word/settings.xml"))
        self.assertEqual(settings.findall("w:trackRevisions", NS), [])

    def test_keep_tracking_flag_retains_settings_bytes(self) -> None:
        make_fixture(self.source, REPLACEMENT)
        self.run_helper("reject", "--keep_tracking_on")
        with zipfile.ZipFile(self.source) as source, zipfile.ZipFile(self.output) as output:
            self.assertEqual(source.read("word/settings.xml"), output.read("word/settings.xml"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
