#!/usr/bin/env python3
"""Export the app's exact legal strings and synchronize the two static pages.

Requires macOS/Xcode's Swift toolchain. Only reads the app repository.
Usage: python3 scripts/sync_legal.py [--app ../Todd] [--check]
"""
import argparse
import html
import json
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- LEGAL_CONTENT_START -->'
END = '<!-- LEGAL_CONTENT_END -->'


def export_app(app):
    source = app / 'Todd'
    # Legal copy is self-contained; no subscription or daily-goal constants.
    swift = (source / 'LegalContent.swift').read_text() + '\n' + """
let payload: [String: Any] = [
    "effectiveDate": LegalContent.effectiveDate,
    "supportEmail": LegalContent.supportEmail,
    "privacy": LegalContent.privacySections.map { ["title": $0.title, "body": $0.body] },
    "terms": LegalContent.termsSections.map { ["title": $0.title, "body": $0.body] }
]
let data = try JSONSerialization.data(withJSONObject: payload, options: [.prettyPrinted, .sortedKeys, .withoutEscapingSlashes])
FileHandle.standardOutput.write(data)
"""
    with tempfile.TemporaryDirectory(prefix='swole-legal-') as directory:
        path = Path(directory) / 'export.swift'
        path.write_text(swift)
        return json.loads(subprocess.check_output(['swift', str(path)], text=True))


def render(sections):
    ids = [f'section-{i+1}' for i in range(len(sections))]
    toc = '<details class="contents"><summary>On this page</summary><nav aria-label="Document sections">'
    toc += ''.join(f'<a href="#{key}">{html.escape(s["title"])}</a>' for key, s in zip(ids, sections))
    toc += '</nav></details>\n<div class="legal-copy">\n'
    for key, section in zip(ids, sections):
        paragraphs = ''.join('<p>' + html.escape(p) + '</p>' for p in section['body'].split('\n\n'))
        # Link the existing email without changing its visible text.
        paragraphs = paragraphs.replace('support@toddlabs.info', '<a href="mailto:support@toddlabs.info">support@toddlabs.info</a>')
        toc += f'<section class="legal-section" id="{key}"><h2>{html.escape(section["title"])}</h2>{paragraphs}</section>\n'
    return toc + '</div>'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', type=Path, default=ROOT.parent / 'Todd')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = export_app(args.app.resolve())
    mismatch = []
    snapshot = ROOT / 'legal-content.json'
    if args.check:
        if json.loads(snapshot.read_text()) != data:
            mismatch.append(snapshot.name)
    else:
        snapshot.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    for name in ['privacy', 'terms']:
        path = ROOT / (name + '.html')
        original = path.read_text()
        if original.count(START) != 1 or original.count(END) != 1:
            raise SystemExit(f'{path.name}: expected exactly one legal content region')
        before, rest = original.split(START)
        _, after = rest.split(END)
        expected = before + START + '\n' + render(data[name]) + '\n' + END + after
        expected = re.sub(r'(<span data-legal-date>).*?(</span>)', lambda m: m[1] + html.escape(data['effectiveDate']) + m[2], expected)
        if args.check:
            if expected != original:
                mismatch.append(path.name)
        else:
            path.write_text(expected)
    if mismatch:
        raise SystemExit('Legal content is out of sync: ' + ', '.join(mismatch))
    print(f'{"Verified" if args.check else "Synced"}: {len(data["privacy"])} privacy sections and {len(data["terms"])} terms sections match the app, including the effective date.')


if __name__ == '__main__':
    main()
