"""Check the actual built site's internal routes, media and metadata."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys

root = Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
pages = [root/'index.html',root/'404.html',*sorted((root/'projects').glob('*/index.html'))]
class Document(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.ids=[];self.h1=0;self.lang=False;self.title=False;self.description=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html': self.lang=a.get('lang')=='zh-CN'
        if tag=='title':self.title=True
        if tag=='h1':self.h1+=1
        if tag=='meta' and a.get('name')=='description':self.description=bool(a.get('content'))
        if a.get('id'):self.ids.append(a['id'])
        if tag=='img':assert a.get('alt'), 'Image missing alternative text'
        if tag=='a' and a.get('target')=='_blank':assert 'noopener' in a.get('rel',''), 'External link missing noopener'
        for key in ['href','src','poster']:
            if a.get(key):self.links.append(a[key])

docs={}
for path in pages:
    assert path.exists(),f'Missing {path}'
    doc=Document();doc.feed(path.read_text(encoding='utf-8'));docs[path]=doc
    assert doc.lang and doc.title and doc.description and doc.h1==1,f'Missing page semantics: {path}'
    assert len(doc.ids)==len(set(doc.ids)),f'Duplicate IDs in {path}'
for path,doc in docs.items():
    for url in doc.links:
        u=urlsplit(url)
        if u.scheme or u.netloc:continue
        target=(root/unquote(u.path).lstrip('/')) if u.path.startswith('/') else path.parent/unquote(u.path)
        if not u.path:target=path
        if target.is_dir():target=target/'index.html'
        assert target.exists(),f'Broken link {url} in {path}'
        if u.fragment and target in docs:assert u.fragment in docs[target].ids,f'Broken anchor {url} in {path}'
print(f'PASS: {len(pages)} pages; internal routes, anchors, media, metadata, accessibility semantics.')
