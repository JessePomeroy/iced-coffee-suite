#!/usr/bin/env python3
"""Report or resolve inline tracked revisions in a DOCX main document part."""

from __future__ import annotations

import argparse
from io import BytesIO
from pathlib import Path
import sys
import zipfile

from lxml import etree


WORD = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
KINDS = ("ins", "del", "moveTo", "moveFrom")
DOCUMENT = "word/document.xml"
SETTINGS = "word/settings.xml"


def parse_xml(data: bytes) -> etree._Element:
    return etree.fromstring(data, parser=etree.XMLParser(resolve_entities=False, no_network=True))


def counts(document: etree._Element) -> dict[str, int]:
    return {kind: sum(1 for _ in document.iter(WORD + kind)) for kind in KINDS}


def resolve(document: etree._Element, decision: str) -> None:
    retained = {WORD + kind for kind in (("ins", "moveTo") if decision == "accept" else ("del", "moveFrom"))}
    # Children are resolved before any enclosing revision is retained or removed.
    for revision in reversed(list(document.iter())):
        if revision.tag not in {WORD + kind for kind in KINDS}:
            continue
        parent = revision.getparent()
        if parent is None:
            continue
        index = parent.index(revision)
        if revision.tag in retained:
            if decision == "reject":
                for text in revision.iter(WORD + "delText"):
                    text.tag = WORD + "t"
            parent[index : index + 1] = list(revision)
        else:
            parent.remove(revision)


def xml_bytes(element: etree._Element) -> bytes:
    return etree.tostring(element, encoding="UTF-8", xml_declaration=True, standalone=True)


def process(source: Path, destination: Path | None, mode: str, keep_tracking: bool) -> None:
    if destination is not None:
        if destination.resolve() == source.resolve():
            raise ValueError("Choose a separate output path; the source must remain unchanged")
        if destination.exists() or destination.is_symlink():
            raise ValueError(f"Output already exists: {destination}")
    with zipfile.ZipFile(source) as package:
        document = parse_xml(package.read(DOCUMENT))
        print(" ".join(f"{kind}={value}" for kind, value in counts(document).items()))
        if mode == "report":
            return
        resolve(document, mode)
        replacements = {DOCUMENT: xml_bytes(document)}
        if not keep_tracking and SETTINGS in package.namelist():
            settings = parse_xml(package.read(SETTINGS))
            switches = list(settings.iter(WORD + "trackRevisions"))
            for switch in switches:
                switch.getparent().remove(switch)
            if switches:
                replacements[SETTINGS] = xml_bytes(settings)
        # Finish the archive in memory before exclusively creating the requested file.
        assembled = BytesIO()
        with zipfile.ZipFile(assembled, "w") as result:
            result.comment = package.comment
            for part in package.infolist():
                payload = replacements[part.filename] if part.filename in replacements else package.read(part)
                result.writestr(part, payload)
    if destination is None:
        raise ValueError("--out is required for accept/reject")
    with destination.open("xb") as output:
        output.write(assembled.getvalue())
    print(f"{mode}: wrote {destination}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("in_docx", type=Path)
    parser.add_argument("--mode", required=True, choices=("report", "accept", "reject"))
    parser.add_argument("--out", type=Path)
    parser.add_argument("--keep_tracking_on", action="store_true")
    options = parser.parse_args()
    if options.mode != "report" and options.out is None:
        parser.error("--out is required for accept/reject")
    try:
        process(options.in_docx, options.out if options.mode != "report" else None,
                options.mode, options.keep_tracking_on)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, etree.XMLSyntaxError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
