#!/usr/bin/env python3
"""Build the static GitHub Pages site using only Python's standard library."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CV = 'https://www.dropbox.com/s/jrlijhclnd26m2x/CV_Linjun_Zhang.pdf?dl=0'
SCHOLAR = 'https://scholar.google.com/citations?user=TUAzs3sAAAAJ&hl=en&sortby=pubdate'
EMAIL = 'linjun.zhang@rutgers.edu'
PROFILE = json.loads((ROOT / 'data/profile.json').read_text())
PAPERS = json.loads((ROOT / 'data/publications.json').read_text())

def link(url, text, extra=''):
    return f'<a href="{escape(url, quote=True)}"{extra}>{text}</a>'

def shell(name, body, description):
    filename = 'index.html' if name == 'Home' else f'{name}.html'
    title = 'Linjun Zhang | Statistics · Rutgers University' if name == 'Home' else f'{name} | Linjun Zhang'
    nav = ''.join(link('index.html' if n == 'Home' else f'{n}.html', n, ' aria-current="page"' if n == name else '') for n in ['Home','About','Research','People','Teaching','Software'])
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{escape(description, quote=True)}">
  <link rel="canonical" href="https://linjunz.github.io/{'' if name == 'Home' else filename}">
  <link rel="icon" href="icon.jpg" type="image/jpeg">
  <link rel="stylesheet" href="assets/site.css?v=service-2">
  <script src="assets/site.js" defer></script>
</head>
<body data-page="{name}">
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-inner">
  <a class="brand" href="index.html"><span class="monogram" aria-hidden="true">LZ</span>Linjun Zhang</a>
  <button class="menu-toggle" type="button" aria-controls="primary-navigation" aria-expanded="false" hidden>Menu</button>
  <nav class="nav" id="primary-navigation" aria-label="Main navigation">{nav}{link(CV,'CV ↗',' class="cv-link"')}</nav>
</div></header>
<main id="main" class="wrap">{body}</main>
<footer class="site-footer"><div class="wrap footer-inner"><span>© {PROFILE['updated'][:4]} Linjun Zhang</span><span>{link('mailto:'+EMAIL,EMAIL)} · Updated {PROFILE['updated_label']}</span></div></footer>
</body>
</html>
'''
    (ROOT / filename).write_text(html)

def opportunity():
    return f'''<aside class="opportunity" aria-label="Research opportunities"><h2>Join our research</h2><p>I am looking for PhD students starting in <strong>Fall {PROFILE['recruiting_year']}</strong> and research interns. If you are interested, please email me with your CV.</p>{link('mailto:'+EMAIL,'Get in touch ↗')}</aside>'''

def paper_item(p, compact=False):
    title = escape(p['title'])
    if p['url']:
        title = link(p['url'], title)
    authors = escape(p['authors']).replace('Linjun Zhang', '<strong>Linjun Zhang</strong>')
    extra = ''.join(link(l['url'],escape(l['label'])) for l in p.get('extra_links',[]))
    venue = escape(p['venue'])
    if p.get('venue_note'):
        venue = f'{escape(p["venue_note"])} <strong>{venue}</strong>'
    return f'''<li class="paper"><div class="paper-meta">{p['year']} <span aria-hidden="true">/</span> {venue}</div><h3>{title}</h3>{'' if compact else f'<p class="authors">{authors}</p>'}{f'<div class="paper-links">{extra}</div>' if extra else ''}</li>'''

def research_summary():
    return 'My research connects statistical foundations with trustworthy and efficient AI. My recent research interests include efficient AI evaluation, AI safety (including data privacy, copyright, and algorithmic bias), statistical principles of AI agents, and representation learning.'

def research_support():
    return f'''My research is partially supported by NSF CAREER {link('https://www.nsf.gov/awardsearch/showAward?AWD_ID=2340241','DMS-2340241')} (PI); NSF {link('https://www.nsf.gov/awardsearch/showAward?AWD_ID=2413107','DMS-2413107')} (co-PI); and the Renaissance Philanthropy {link('https://www.renaissancephilanthropy.org/crowdsourcing-and-reinventing-the-next-generation-of-dynamic-and-scalable-math-benchmarks','AI for Math Fund')} (co-PI).'''

def academic_service():
    groups = json.loads((ROOT / 'data/service.json').read_text())
    content = '<div class="service-groups">'
    for group in groups:
        list_class = ' class="service-inline"' if group.get('layout') == 'inline' else ''
        content += f'<section class="service-group"><h3>{escape(group["role"])}</h3><ul{list_class}>'
        for item in group['entries']:
            name = escape(item['name'])
            if item.get('url'):
                name = link(item['url'], name)
            details = ''.join(f'<span class="service-detail">{escape(detail)}</span>' for detail in item.get('details', []))
            note = f' ({escape(item["note"])})' if item.get('note') else ''
            label = f'<strong>{escape(item["label"])}</strong>: ' if item.get('label') else ''
            extra_links = ''.join(f'<span class="service-detail">{link(extra["url"], escape(extra["label"]))}</span>' for extra in item.get('extra_links', []))
            content += f'<li>{label}{name}{note}{details}{extra_links}</li>'
        content += '</ul></section>'
    return content + '</div>'

def intro(eyebrow,title,description):
    return f'<header class="page-intro"><p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p>{description}</p></header>'

def side_layout(sections,content):
    links=''.join(link('#'+i,escape(n)) for i,n in sections)
    return f'<div class="page-layout"><nav class="page-nav" aria-label="On this page"><strong>On this page</strong>{links}</nav><div>{content}</div></div>'

def home():
    recent = [next(p for p in PAPERS if p['title'].startswith(t)) for t in ['Evaluating LLMs When They Do Not Know the Answer', 'Contrastive Learning on Multimodal Analysis of Electronic Health Records', 'An Overview of Large Language Models for Statisticians']]
    body = f'''<section class="home-hero" aria-labelledby="name">
<div class="hero-copy">
<h1 id="name">Linjun Zhang</h1>
<p class="position">Associate Professor of Statistics<span>{link('https://statistics.rutgers.edu/','Department of Statistics')}, Rutgers University</span></p>
<p class="intro">{research_summary()}</p>
<p class="intro">I received my Ph.D. in Statistics from the University of Pennsylvania in 2019, advised by {link('http://www-stat.wharton.upenn.edu/~tcai/','T. Tony Cai')}.</p>
<div class="contact-links">{link('mailto:'+EMAIL,'Email ↗')}{link(SCHOLAR,'Google Scholar ↗')}{link(CV,'Curriculum vitae ↗')}</div></div>
<figure class="portrait"><img src="assets/portrait-natural.jpg" width="600" height="900" alt="Portrait of Linjun Zhang" fetchpriority="high"></figure>
</section>
<section class="split-section" aria-labelledby="interests"><div><span class="section-number">01 / RESEARCH</span><h2 id="interests">Research interests</h2></div><div class="topics">
<div class="topic">Efficient AI evaluation<span>Statistical efficiency · Evaluation reliability</span></div><div class="topic">AI safety<span>Data privacy · Statistical watermarking · Algorithmic bias</span></div><div class="topic">AI agents<span>Statistical principles of harness engineering</span></div><div class="topic">Representation learning<span>Self-supervision · Learning theory</span></div>
</div></section>
<section class="split-section" aria-labelledby="recent"><div><span class="section-number">02 / PAPERS</span><h2 id="recent">Highlighted recent work</h2>{link('Research.html','All research ↗',' class="link-arrow"')}</div><ul class="paper-list home-recent">{''.join(paper_item(p,True) for p in recent)}</ul></section>
<section class="split-section" aria-labelledby="support"><div><span class="section-number">03 / SUPPORT</span><h2 id="support">Research support</h2></div><p class="funding">{research_support()}</p></section>
<section class="split-section" aria-labelledby="service"><div><span class="section-number">04 / SERVICE</span><h2 id="service">Academic service</h2></div>{academic_service()}</section>
{opportunity()}'''
    shell('Home', body, 'Linjun Zhang, Associate Professor of Statistics at Rutgers University. Statistical foundations for trustworthy and efficient AI: evaluation, safety, agents, and representation learning.')

def research():
    sections=[]; content=''
    years=sorted({p['year'] for p in PAPERS},reverse=True)
    groups=[(str(y),[p for p in PAPERS if p['year']==y]) for y in years if y>=2021]
    groups.append(('2020 & earlier',[p for p in PAPERS if p['year']<=2020]))
    for label,papers in groups:
        sid='year-'+label[:4]; sections.append((sid,label))
        content+=f'<section id="{sid}" class="content-section"><h2>{escape(label)}</h2><ul class="paper-list">'+''.join(paper_item(p) for p in papers)+'</ul></section>'
    body=intro('Publications &amp; preprints','Research',f'Statistical foundations for trustworthy and efficient AI: efficient evaluation, AI safety, AI agents, and representation learning. {link(SCHOLAR,"Google Scholar ↗")}')
    body+='<p class="small-note">* indicates alphabetical authorship; ** indicates equal contribution. Preprints are labeled separately from published work.</p>'
    body+=side_layout(sections,content)
    shell('Research',body,'Publications and preprints by Linjun Zhang on efficient AI evaluation, AI safety, statistical principles of AI agents, and representation learning.')

def about():
    content=f'''<section class="content-section prose" id="biography"><h2>Biography</h2>
<p>I am an Associate Professor in the {link('https://statistics.rutgers.edu/','Department of Statistics')} at Rutgers University. I received my Ph.D. in Statistics from the University of Pennsylvania in 2019, where I was fortunate to be advised by Professor {link('http://www-stat.wharton.upenn.edu/~tcai/','T. Tony Cai')}.</p>
<p>{research_summary()}</p>
<p>{research_support()}</p>
<p>{link(CV,'View curriculum vitae ↗')}</p></section>
<section class="content-section" id="service"><h2>Academic service</h2>{academic_service()}</section>
<section class="content-section" id="education"><h2>Education</h2>
<div class="timeline-entry"><time>2019</time><h3>Ph.D. in Statistics</h3><p>University of Pennsylvania</p><p>Advisor: T. Tony Cai</p></div>
<div class="timeline-entry"><time>2014</time><h3>B.S. in Statistics</h3><p>University of Science and Technology of China (USTC)</p><p>Hua Loo-Keng Talent Program in Mathematics</p><p>Guo-Moruo Award · summa cum laude, top 1%</p></div></section>
<section class="content-section" id="experience"><h2>Research experience</h2>
<div class="timeline-entry"><time>Summer 2018</time><h3>Bell Labs</h3><p>Research Intern</p></div>
<div class="timeline-entry"><time>Summer 2013</time><h3>University of Western Australia</h3><p>Undergraduate Research Assistant</p></div></section>'''
    body=intro('Background','About',f'Associate Professor of Statistics at Rutgers University. {link("mailto:"+EMAIL,EMAIL)}')
    body+=side_layout([('biography','Biography'),('service','Academic service'),('education','Education'),('experience','Research experience')],content)
    shell('About',body,'Biography, academic service, education, research interests, and experience of Linjun Zhang at Rutgers University.')

def people():
    people=json.loads((ROOT/'data/people.json').read_text())
    students=[p for p in people if p['section']=='PhD students' and not p['details']]
    alumni=[p for p in people if p['section']=='PhD students' and p['details']]
    interns=[p for p in people if p['section']!='PhD students']
    content='<section class="content-section" id="phd"><h2>PhD students</h2><div class="people-grid">'
    content+=''.join(f'<div class="person"><h3>{escape(p["name"])}</h3></div>' for p in students)+'</div></section>'
    content+='<section class="content-section" id="alumni"><h2>PhD alumni</h2><ul class="person-list">'
    for p in alumni:
        name=link(p['links'][0]['url'],escape(p['name'])) if p['links'] else escape(p['name'])
        content+=f'<li><h3>{name}</h3><p>{escape(p["details"].strip("()"))}</p>'+''.join('<p>'+escape(t)+'</p>' for t in p['lines'])+'</li>'
    content+='</ul></section><section class="content-section" id="interns"><h2>Undergraduate &amp; master’s research interns</h2><ul class="person-list">'
    for p in interns:
        lines=''
        for t in p['lines']:
            for l in p['links']:
                if l['label'] in t:
                    t=t.replace(l['label'],'__PAPER__')
                    t=escape(t).replace('__PAPER__',link(l['url'],escape(l['label']))); break
            else: t=escape(t)
            lines+=f'<p>{t}</p>'
        content+=f'<li><h3>{escape(p["name"])}</h3><p>{escape(p["details"])}</p>{lines}</li>'
    content+='</ul></section>'
    body=intro('Students &amp; collaborators','People','I have been very fortunate to work with amazing students and collaborators. We look forward to having more talented students join us.')
    body+=opportunity()+side_layout([('phd','PhD students'),('alumni','PhD alumni'),('interns','Research interns')],content)
    shell('People',body,f'Students, alumni, and research interns working with Linjun Zhang. Recruiting PhD students for Fall {PROFILE["recruiting_year"]}.')

def teaching():
    courses=json.loads((ROOT/'data/teaching.json').read_text())
    sections=[('rutgers','Instructor at Rutgers'),('wharton','Instructor at Wharton'),('recitation','Recitation Instructor'),('assistant','Teaching Assistant')]
    content=''
    for sid,label in sections:
        selected=[c for c in courses if c['section']==label]
        if sid=='rutgers': selected=list(reversed(selected))
        content+=f'<section class="content-section" id="{sid}"><h2>{label}</h2><ul class="course-list">'
        for c in selected:
            m=re.match(r'(STAT [0-9/]+)\s*,\s*(.*?),\s*((?:Fall|Spring|Summer).*)',c['title'])
            code,title,term=m.groups() if m else ('',c['title'],'')
            details=''.join(f'<p>{escape(d)}</p>' for d in c['details'] if not d.startswith('['))
            links=' · '.join(link(l['url'],escape(l['label'])) for l in c['links'])
            content+=f'<li class="course"><time>{escape(term)}</time><div><div class="course-code">{escape(code)}</div><h3>{escape(title)}</h3>{details}{f"<p>{links}</p>" if links else ""}</div></li>'
        content+='</ul></section>'
    body=intro('Courses &amp; instruction','Teaching','Course offerings at Rutgers University and earlier teaching at the Wharton School, University of Pennsylvania.')
    body+=side_layout(sections,content)
    shell('Teaching',body,'Courses taught by Linjun Zhang at Rutgers University and the Wharton School, University of Pennsylvania.')

def software():
    projects=json.loads((ROOT/'data/software.json').read_text())
    content='<div class="software-grid">'
    for p in projects:
        paper=link(p['paper'],'Paper ↗') if p.get('paper') else ''
        content+=f'<article class="software"><span class="language">{escape(p["language"])}</span><h2>{link(p["url"],escape(p["name"]))}</h2><p>{escape(p["description"])}</p><div class="software-links">{link(p["url"],"Code on GitHub ↗")}{paper}</div></article>'
    content+='</div>'
    body=intro('Code &amp; implementations','Software','Software accompanying our research in statistical learning, fairness, robustness, and meta-learning.')+content
    shell('Software',body,'Research software by Linjun Zhang and collaborators: CHIME, ADAM, MLTI, MetaMIX, LISA, and FaiREE.')

if __name__ == '__main__':
    for build in [home,about,research,people,teaching,software]: build()
    print(f'Built 6 static pages and {len(PAPERS)} unique research entries.')
