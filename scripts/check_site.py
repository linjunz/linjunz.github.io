#!/usr/bin/env python3
"""Check HTML structure, navigation, assets, content counts, and publication uniqueness."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import json
ROOT=Path(__file__).resolve().parents[1]
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Check(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.ids=set(); self.refs=[]; self.h1=0; self.current=0; self.main=0; self.lang=False; self.errors=[]; self.in_a=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html': self.lang=bool(a.get('lang'))
        if tag=='h1': self.h1+=1
        if tag=='main': self.main+=1
        if a.get('aria-current')=='page': self.current+=1
        if a.get('id'):
            if a['id'] in self.ids: self.errors.append('Duplicate ID: '+a['id'])
            self.ids.add(a['id'])
        if tag=='a' and self.in_a: self.errors.append('Nested anchor')
        if tag=='a': self.in_a=True
        if tag=='img' and not a.get('alt'): self.errors.append('Image missing alt text')
        for k in ('href','src'):
            if k in a: self.refs.append(a[k])
        if tag not in VOID: self.stack.append(tag)
    def handle_endtag(self,tag):
        if tag in VOID: return
        if tag=='a': self.in_a=False
        if not self.stack or self.stack[-1]!=tag: self.errors.append('Mismatched close: '+tag)
        else: self.stack.pop()

pages={}
for name in ['index','About','Research','People','Teaching','Software']:
    path=ROOT/(name+'.html'); c=Check(); c.feed(path.read_text()); pages[path.name]=c
    assert not c.errors and not c.stack,(name,c.errors,c.stack)
    assert c.h1==c.main==c.current==1,(name,'landmarks/current-page')
    assert c.lang,(name,'language')
for name,c in pages.items():
    for ref in c.refs:
        u=urlparse(ref)
        assert not u.scheme or u.scheme in ('https','http','mailto'),(name,ref)
        if u.scheme or u.netloc: continue
        path=ROOT/unquote(u.path.lstrip('/')) if u.path else ROOT/name
        assert path.exists(),(name,'Missing local target',ref)
        if u.fragment and path.suffix=='.html': assert u.fragment in pages[path.name].ids,(name,ref)
papers=json.loads((ROOT/'data/publications.json').read_text())
keys=[p['url'] or p['title'].lower() for p in papers]
assert len(keys)==len(set(keys)),'Duplicate paper'
assert all(p['year'] and p['title'] and p['authors'] and p['venue'] for p in papers)
assert all('Linjun Zhang' in p['authors'] or 'L. Zhang' in p['authors'] for p in papers),'Check authors'
assert all(str(p['year']) in (ROOT/'Research.html').read_text() for p in papers)
for name in ['index.html','People.html']:
    assert 'Fall 2027' in (ROOT/name).read_text()
assert (ROOT/'Research.html').read_text().count('class="paper"')==len(papers)
assert (ROOT/'Teaching.html').read_text().count('class="course"')==18
assert (ROOT/'Software.html').read_text().count('class="software"')==6
print(f'PASS: {len(pages)} pages; {len(papers)} unique papers; 18 courses; 6 software projects; all local links, IDs, and HTML structure.')
