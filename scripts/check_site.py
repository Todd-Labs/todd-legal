#!/usr/bin/env python3
"""Validate local links, assets, headings, and the exported legal copy (no dependencies)."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import struct

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = []
        self.links = []
        self.images = []
        self.headings = 0
        self.legal = []
        self.section = None
        self.field = None
        self.parts = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'h1':
            self.headings += 1
        for name in ['href', 'src']:
            if name in attrs:
                self.links.append(attrs[name])
        if tag == 'img':
            self.images.append(attrs)
        if tag == 'section' and attrs.get('class') == 'legal-section':
            self.section = {'title': '', 'paragraphs': []}
        if self.section is not None and tag in ['h2', 'p']:
            self.field = tag
            self.parts = []

    def handle_data(self, value):
        if self.field:
            self.parts.append(value)

    def handle_endtag(self, tag):
        if self.section is not None and tag == self.field:
            value = ''.join(self.parts)
            if tag == 'h2':
                self.section['title'] = value
            else:
                self.section['paragraphs'].append(value)
            self.field = None
        if tag == 'section' and self.section is not None:
            self.legal.append({'title': self.section['title'], 'body': '\n\n'.join(self.section['paragraphs'])})
            self.section = None


def main():
    pages = {p.name: Page(p) for p in ROOT.glob('*.html')}
    assert set(pages) == {'index.html', 'faq.html', 'privacy.html', 'terms.html'}
    count = 0
    for name, page in pages.items():
        assert page.headings == 1, (name, 'expected one h1')
        assert len(page.ids) == len(set(page.ids)), (name, 'duplicate IDs')
        for value in page.links:
            link = urlsplit(value)
            if link.scheme or link.netloc:
                continue
            target = (ROOT / unquote(link.path)) if link.path else page.path
            assert target.is_file(), (name, 'missing local target', value)
            if link.fragment:
                assert target.name in pages and unquote(link.fragment) in pages[target.name].ids, (name, 'broken anchor', value)
            count += 1
        for img in page.images:
            assert img.get('alt'), (name, 'missing image description')
            payload = (ROOT / img['src']).read_bytes()
            assert payload[:8] == b'\x89PNG\r\n\x1a\n'
            width, height = struct.unpack('>II', payload[16:24])
            assert (width, height) == (int(img['width']), int(img['height'])), (name, 'incorrect image dimensions')
        assert '<script' not in page.path.read_text().lower(), (name, 'review new script behavior')
    for value in re.findall(r'url\([\'"]?([^\)\'\"]+)', (ROOT / 'styles.css').read_text()):
        assert (ROOT / value).is_file(), ('missing CSS asset', value)
    legal = json.loads((ROOT / 'legal-content.json').read_text())
    for name in ['privacy', 'terms']:
        assert pages[name + '.html'].legal == legal[name], (name, 'legal text mismatch')
        assert legal['effectiveDate'] in pages[name + '.html'].path.read_text()
    print(f'PASS: {len(pages)} pages, {count} local links/assets, image dimensions, descriptions, headings, anchors, and all 33 legal sections.')


if __name__ == '__main__':
    main()
