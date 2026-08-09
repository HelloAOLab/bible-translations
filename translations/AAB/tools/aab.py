#!/usr/bin/env python3
"""AAB working tools. Run from translations/AAB/.

  ./tools/aab.py verse "ROM 3:25"     text + footnotes for a verse
  ./tools/aab.py notes "LEV 16:10"    footnotes only
  ./tools/aab.py find "soul"          search running TEXT (footnotes excluded)
  ./tools/aab.py findnotes "kipper"   search footnotes only
  ./tools/aab.py count "purgation"    count in running text, by book
  ./tools/aab.py validate             XML-validate all 66 books
  ./tools/aab.py replace FILE.usx "old" "new"    safe single-match replace + validate

Notes on searching: `find` strips footnotes first, so it reports only what a
reader sees in the translation. This is the check to run before claiming a term
is or is not used in the text.
"""
import glob
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTE_RE = re.compile(r'<note.*?</note>', re.DOTALL)
TAG_RE = re.compile(r'<[^>]+>')


def books():
    return sorted(glob.glob(os.path.join(HERE, '*.usx')))


def read(path, strip_notes=False):
    c = open(path, encoding='utf-8').read()
    return NOTE_RE.sub('', c) if strip_notes else c


def verse_block(content, ref):
    m = re.search(r'sid="%s"(.*?)eid="%s"' % (re.escape(ref), re.escape(ref)),
                  content, re.DOTALL)
    return m.group(0) if m else None


def find_book(ref):
    code = ref.split()[0].upper()
    path = os.path.join(HERE, code + '.usx')
    if not os.path.exists(path):
        sys.exit('No such book: %s' % code)
    return path, '%s %s' % (code, ref.split(None, 1)[1])


def clean_text(block):
    """Strip footnotes, the leading sid fragment, and the trailing eid fragment."""
    t = NOTE_RE.sub('', block)
    t = re.sub(r'^sid="[^"]*"\s*/>', '', t)
    t = re.sub(r'<verse\s+eid="[^"]*"\s*$', '', t)
    return re.sub(r'\s+', ' ', TAG_RE.sub(' ', t)).strip()


def cmd_verse(ref):
    path, ref = find_book(ref)
    block = verse_block(read(path), ref)
    if not block:
        sys.exit('Verse not found: %s' % ref)
    print('%s\n  %s' % (ref, clean_text(block)))
    notes = re.findall(r'<char style="ft">(.*?)</char>', block, re.DOTALL)
    for n in notes:
        print('  [fn] %s' % n)
    if not notes:
        print('  (no footnotes)')


def cmd_notes(ref):
    path, ref = find_book(ref)
    block = verse_block(read(path), ref)
    if not block:
        sys.exit('Verse not found: %s' % ref)
    for n in re.findall(r'<char style="ft">(.*?)</char>', block, re.DOTALL):
        print(n)


def _scan(pattern, strip_notes):
    rx = re.compile(pattern, re.IGNORECASE)
    hits = 0
    for path in books():
        content = read(path, strip_notes=strip_notes)
        for m in re.finditer(r'sid="([^"]+)"[^>]*/>((?:(?!<verse).)*?)(?=<verse|\Z)',
                             content, re.DOTALL):
            body = re.sub(r'\s+', ' ', TAG_RE.sub(' ', m.group(2)))
            if rx.search(body):
                snip = rx.search(body)
                s = max(0, snip.start() - 45)
                print('%-14s ...%s...' % (m.group(1), body[s:snip.end() + 35].strip()))
                hits += 1
    print('\n%d verse(s)' % hits)


def cmd_find(pattern):
    _scan(pattern, strip_notes=True)


def cmd_findnotes(pattern):
    rx = re.compile(pattern, re.IGNORECASE)
    hits = 0
    for path in books():
        code = os.path.basename(path).replace('.usx', '')
        for m in re.finditer(r'<char style="fr">(.*?)</char><char style="ft">(.*?)</char>',
                             read(path), re.DOTALL):
            if rx.search(m.group(2)):
                print('%s %s :: %s' % (code, m.group(1).strip(), m.group(2)[:150]))
                hits += 1
    print('\n%d footnote(s)' % hits)


def cmd_count(pattern):
    rx = re.compile(pattern, re.IGNORECASE)
    total = 0
    for path in books():
        n = len(rx.findall(TAG_RE.sub(' ', read(path, strip_notes=True))))
        if n:
            print('%6d  %s' % (n, os.path.basename(path).replace('.usx', '')))
            total += n
    print('%6d  TOTAL (running text only)' % total)


def cmd_validate():
    bad = []
    for path in books():
        try:
            ET.parse(path)
        except Exception as e:
            bad.append((os.path.basename(path), e))
    for name, err in bad:
        print('FAIL %s: %s' % (name, err))
    print('%d/%d books valid' % (len(books()) - len(bad), len(books())))
    return 1 if bad else 0


def cmd_replace(fname, old, new):
    path = os.path.join(HERE, os.path.basename(fname))
    c = open(path, encoding='utf-8').read()
    n = c.count(old)
    if n != 1:
        sys.exit('Refusing: found %d matches (need exactly 1) for:\n  %s' % (n, old[:120]))
    open(path, 'w', encoding='utf-8').write(c.replace(old, new))
    try:
        ET.parse(path)
    except Exception as e:
        sys.exit('XML INVALID after edit: %s' % e)
    if '—' in new:
        print('WARNING: new text contains an em dash (house style forbids it)')
    print('Replaced 1 occurrence in %s; XML valid' % os.path.basename(path))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd, args = sys.argv[1], sys.argv[2:]
    fns = {'verse': cmd_verse, 'notes': cmd_notes, 'find': cmd_find,
           'findnotes': cmd_findnotes, 'count': cmd_count,
           'validate': cmd_validate, 'replace': cmd_replace}
    if cmd not in fns:
        sys.exit(__doc__)
    sys.exit(fns[cmd](*args) or 0)


if __name__ == '__main__':
    main()
