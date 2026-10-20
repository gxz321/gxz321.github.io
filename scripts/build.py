"""Pre-render GXZ's English research portfolio. Python standard library only."""
from pathlib import Path
import argparse
import html
import json
import shutil
import hashlib

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://gxz321.github.io"
PROFILE = json.loads((ROOT / "content/profile.json").read_text(encoding="utf-8"))
PROJECTS = json.loads((ROOT / "content/projects.json").read_text(encoding="utf-8"))
e = html.escape

def asset_url(path):
    source=(ROOT/path.lstrip('/')).read_bytes().replace(b'\r\n',b'\n')
    return path+'?v='+hashlib.sha256(source).hexdigest()[:10]

def arrow(direction="right"):
    paths = {"right": "M4 12h16M13 5l7 7-7 7", "up": "M5 19 19 5M5 5h14v14", "down": "M12 4v16M5 13l7 7 7-7"}
    return f'<svg class="arrow-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="{paths[direction]}" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def nav():
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header id="top" class="site-header wrap">
<a class="brand" href="/" aria-label="GXZ home">GXZ<span>.</span></a><span class="brand-note">independent research</span>
<button class="menu-toggle" aria-expanded="false" aria-controls="main-nav"><span data-menu-label>Menu</span><span class="menu-mark" aria-hidden="true"></span></button>
<nav id="main-nav" class="main-nav" aria-label="Main navigation"><a class="nav-link" href="/#projects">Work <span>(03)</span></a><a class="nav-link" href="/#approach">Approach</a><a class="nav-link" href="/#about">About</a><a class="nav-link" href="/#contact">Contact {arrow('up')}</a></nav></header>'''

def footer():
    return f'''<footer class="site-footer" id="contact"><div class="wrap">
<div class="contact-grid"><h2>Let’s make<br>sense of it.</h2><a class="contact-link" href="https://github.com/gxz321" target="_blank" rel="noopener noreferrer"><span class="circle-arrow" data-magnetic>{arrow()}</span><span>Find me on GitHub {arrow('up')}</span></a></div>
<div class="footer-line"><span>© 2026 GXZ</span><span>RESEARCH / DESIGN / EXPERIMENTS</span><a href="#top">Back to top ↑</a></div></div></footer>'''

def page(title, description, body, path="/", image="/assets/portfolio/social-preview.png", schema=None, bodyclass=""):
    structured = json.dumps(schema or {"@context":"https://schema.org", "@type":"WebSite", "name":"GXZ — Intelligence, in motion.", "url":SITE}, ensure_ascii=False).replace("<", "\\u003c")
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f3f4ef">
<title>{e(title)}</title><meta name="description" content="{e(description, quote=True)}"><link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website"><meta property="og:locale" content="en_US"><meta property="og:site_name" content="GXZ"><meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(description,quote=True)}"><meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{SITE}{image}"><meta name="twitter:card" content="summary_large_image">
<script>document.documentElement.classList.add('js')</script>
<link rel="icon" type="image/svg+xml" href="/assets/portfolio/favicon.svg"><link rel="preload" href="/assets/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{asset_url('/assets/css/portfolio.css')}"><script src="{asset_url('/assets/js/motion.js')}" defer></script><script src="{asset_url('/assets/js/portfolio.js')}" defer></script>
<script type="application/ld+json">{structured}</script></head><body class="{bodyclass}">{nav()}{body}{footer()}</body></html>'''

def cover(p):
    return "/assets/portfolio/crowd-paths.svg" if p["slug"] == "crowdflow-ai" else p["cover"]

def work_link(p, cls="case-link"):
    return f'<a class="{cls}" href="/projects/{p["slug"]}/" aria-label="View case study: {e(p["title"],quote=True)}"><span class="circle-arrow" data-magnetic>{arrow()}</span><span>View case study</span></a>'

def secondary_project(p):
    subtitle = "A testable bridge between robot policies and simulation." if p["slug"] == "groot" else "Field observation, spatial reconstruction, and pedestrian paths."
    status = "Engineering in progress." if p["slug"] == "groot" else "Course research."
    image = cover(p) if p["slug"] == "groot" else "/assets/portfolio/sunken-site.webp"
    image_alt = p['coverAlt'] if p["slug"] == "groot" else "Daytime observation of the campus sunken plaza"
    return f'''<article class="project-study" data-reveal>
<a class="study-media" href="/projects/{p['slug']}/" aria-label="Open {e(p['title'],quote=True)} case study"><img src="{image}" width="1440" height="1000" alt="{e(image_alt,quote=True)}" loading="lazy"></a>
<div class="study-index"><span>{p['index']}</span><span>{p['year']}</span></div><h3>{e(p['title'])}</h3><p class="study-subtitle">{subtitle}</p><p class="study-status mono">{status}</p>{work_link(p)}</article>'''

def home():
    p = PROJECTS[0]
    studies = "".join(secondary_project(p) for p in PROJECTS[1:])
    body = f'''<main id="main" tabindex="-1">
<section class="hero wrap" aria-labelledby="hero-heading">
<div class="hero-grid"><h1 class="hero-title" id="hero-heading"><span>Intelligence,</span><span>in <em>motion.</em></span></h1>
<div class="hero-support"><p>{e(PROFILE['statement'])}</p><a class="hero-cta" href="#projects"><span>Explore selected work</span><span class="circle-arrow" data-magnetic>{arrow()}</span></a></div>
<figure class="hero-field"><div class="flow-panel" data-flow-panel><canvas id="hero-flow" data-flow-field data-scheme="dark" aria-hidden="true" width="960" height="720"></canvas><button class="flow-toggle" aria-controls="hero-flow" aria-pressed="false"><span class="pause-mark" aria-hidden="true"></span><span data-flow-label>Pause motion</span></button></div><figcaption>Illustrative flow field · not a calibrated simulation</figcaption></figure></div>
<div class="hero-baseline mono"><span>PEOPLE / SPACE / MACHINES</span><a href="#projects">SCROLL TO EXPLORE ↓</a></div></section>
<section class="selected-work" id="projects" aria-labelledby="work-heading"><div class="wrap section-head" data-reveal><h2 id="work-heading">Selected work <span class="mono">(01—03)</span></h2><p class="mono">Three ways of looking<br>at complex systems.</p></div>
<article class="featured-project" data-reveal><a class="featured-media" href="/projects/crowdflow-ai/" aria-label="Open CrowdFlow AI case study"><img src="/assets/portfolio/crowd-paths.svg" width="1440" height="1000" alt="A selected set of pedestrian trajectories from the TopView 1A recording" loading="lazy"></a><div class="featured-copy"><span class="featured-index mono">01</span><h3>CrowdFlow AI</h3><p>Reading crowds.<br> Rethinking flow.</p><span class="featured-status mono">2026 / Research prototype</span>{work_link(p)}</div></article>
<div class="wrap"><div class="work-pair">{studies}</div><div class="forthcoming"><span class="mono">04</span><h3>Medical robotics</h3><p class="mono">Case study forthcoming.</p><span class="forthcoming-mark" aria-hidden="true">—</span></div></div></section>
<section class="approach wrap" id="approach" aria-labelledby="approach-heading"><h2 id="approach-heading" data-reveal>A way of<br>working.</h2><div class="approach-steps">
<div class="approach-step" data-reveal><span class="mono">01</span><h3>Observe</h3><p class="mono">Start with people, context,<br> and evidence.</p></div>
<div class="approach-step" data-reveal><span class="mono">02</span><h3>Model</h3><p class="mono">Make assumptions visible.<br> Build something testable.</p></div>
<div class="approach-step" data-reveal><span class="mono">03</span><h3>Refine</h3><p class="mono">Compare, question, and<br> keep the limits in view.</p></div></div></section>
<section class="about-band" id="about" aria-labelledby="about-heading"><div class="wrap about-grid"><h2 id="about-heading" data-reveal>Curiosity,<br>made tangible.</h2><div class="about-copy" data-reveal><span class="mono">ABOUT GXZ</span><p>I work between code and space. My projects explore human movement, public places, and embodied intelligence. This is a record of what I build, what I learn, and what still needs testing.</p></div></div></section></main>'''
    return page("GXZ — Intelligence, in motion.", "Independent research at the intersection of crowd movement, public space, and embodied intelligence. Selected projects and experiments by GXZ.", body, bodyclass="home")

def evidence_view(slug):
    if slug == "crowdflow-ai":
        options = [
            ("Trajectories","/assets/portfolio/crowd-paths.svg","Selected trajectories from the TopView 1A recording","A deterministic sample of pedestrian trajectories from one recording. Distances retain the source coordinate scale."),
            ("Relative frequency","/assets/portfolio/crowd-density.svg","Relative observation frequency across the TopView 1A recording","All recorded positions from the same clip, grouped into spatial bins. Relative sample frequency is not calibrated occupancy, density, or risk.")
        ]
        label, note = "One recording, two readings.", "The two views describe one source clip; neither is a calibrated safety assessment."
    elif slug == "sunken-plaza":
        options = [
            ("On site","/assets/portfolio/sunken-site.webp","Fixed-camera view of the campus sunken plaza","A daytime observation frame from the course study."),
            ("Reconstruction","/assets/portfolio/sunken.webp","Reconstructed plaza geometry with pedestrian traces","Reconstructed context and pedestrian visualization from the course study. The viewpoints differ; this is not a registered before-and-after comparison.")
        ]
        label, note = "From observation to spatial context.", "Different viewpoints reveal different parts of the study."
    else:
        return '''<section class="artifact-section" id="artifacts"><div class="artifact-heading"><span class="mono">SYSTEM MAP</span><h3>Three interfaces.<br>One testable workflow.</h3></div><div class="workflow">
<details open><summary><span class="mono">01</span><strong>Dataset</strong><span class="workflow-status">Demonstrations required</span></summary><p>Preflight checks inspect the expected dataset structure. Real SO-101 demonstrations, synchronized cameras, and verified joint units still need to be provided.</p></details>
<details><summary><span class="mono">02</span><strong>Policy</strong><span class="workflow-status">Protocol tested</span></summary><p>The dual-camera HTTP interface, explicit mock and real backends, and joint mapping are implemented. Twelve CPU protocol and validation tests pass. Actual learned-policy inference requires a compatible checkpoint and environment.</p></details>
<details><summary><span class="mono">03</span><strong>Simulation</strong><span class="workflow-status">GPU evaluation pending</span></summary><p>The bounded rollout entry point is written. A calibrated scene, verified assets, real model outputs, and GPU task evaluation remain necessary before reporting robot capability.</p></details></div></section>'''
    buttons = "".join(f'<button type="button" aria-pressed="{str(i==0).lower()}" data-image="{o[1]}" data-alt="{e(o[2],quote=True)}" data-caption="{e(o[3],quote=True)}">{o[0]}</button>' for i,o in enumerate(options))
    o=options[0]; other=options[1]
    return f'''<section class="artifact-section" id="artifacts" data-evidence-view><div class="artifact-heading"><span class="mono">EVIDENCE IN VIEW</span><h3>{label}</h3><p>{note}</p></div><div class="evidence-controls" data-evidence-controls role="group" aria-label="Choose evidence view">{buttons}</div><figure class="evidence-figure"><img data-evidence-image src="{o[1]}" alt="{o[2]}" width="1440" height="1000" loading="lazy"><figcaption data-evidence-caption aria-live="polite">{o[3]}</figcaption></figure><a class="figure-fullsize mono" data-evidence-fullsize href="{o[1]}" target="_blank" rel="noopener noreferrer">Open full-size figure {arrow('up')}</a><noscript><figure class="evidence-figure"><img src="{other[1]}" alt="{other[2]}" width="1440" height="1000" loading="lazy"><figcaption>{other[3]}</figcaption></figure></noscript></section>'''

def detail(p, next_p):
    chapter_names=["The question","The method","What exists","What comes next"]
    chapters=[]
    for i,s in enumerate(p["sections"]):
        heading = s["title"].split(" / ",1)[-1]
        paras = "".join(f"<p>{e(t)}</p>" for t in s["paragraphs"])
        chapters.append(f'<section class="case-section" id="chapter-{i+1}"><span class="chapter-label mono">0{i+1} / {chapter_names[i].upper()}</span><h2>{e(heading)}</h2>{paras}</section>')
        if i==1: chapters.append(evidence_view(p["slug"]))
    toc = "".join(f'<a class="nav-link" href="#chapter-{i+1}">{name}</a>'+('<a class="nav-link" href="#artifacts">Explore the evidence</a>' if i==1 else '') for i,name in enumerate(chapter_names))
    links = "".join('<a href="'+e(l["url"],quote=True)+'" '+('download' if l["url"].endswith(".zip") else 'target="_blank" rel="noopener noreferrer"')+'>'+e(l["label"])+' '+arrow("up")+'</a>' for l in p["links"])
    deliverables = "".join(f"<li>{e(x)}</li>" for x in p.get("deliverables",[]))
    movie = '''<figure class="study-film"><video controls preload="none" playsinline poster="/assets/portfolio/sunken.webp" aria-label="Silent pedestrian visualization in the reconstructed plaza" aria-describedby="film-description"><source src="/assets/portfolio/sunken-flow.mp4" type="video/mp4">Your browser does not support this video. <a href="/assets/portfolio/sunken-flow.mp4">Download the research animation</a>.</video><figcaption id="film-description">Silent research animation. Pedestrian markers and concentrations show sampled movement and gathering areas in the reconstructed plaza. This is an exploratory visualization of the recorded periods. <a class="inline-link" href="/assets/portfolio/sunken-flow.mp4" download>Download the research animation</a>.</figcaption></figure>''' if p["slug"]=="sunken-plaza" else ""
    schema={"@context":"https://schema.org","@type":"CreativeWork","name":p["title"],"description":p["summary"],"url":SITE+"/projects/"+p["slug"]+"/","creativeWorkStatus":p["status"]}
    body=f'''<main id="main" tabindex="-1" class="case-main"><div class="wrap"><a class="back-link mono" href="/#projects">← All projects</a><header class="case-header"><div class="case-title-line"><h1>{e(p['title'])}</h1><span class="mono">{p['index']} / {p['year']}</span></div><p class="case-lead">{e(p['summary'])}</p><dl class="case-facts"><div><dt>FIELD</dt><dd>{e(p['category'].title())}</dd></div><div><dt>STATUS</dt><dd>{e(p['status'])}</dd></div><div><dt>TOOLS</dt><dd>{e(', '.join(p['stack'][:3]))}</dd></div></dl></header>
<figure class="case-cover"><img src="{cover(p)}" width="1440" height="1000" alt="{e(p['coverAlt'],quote=True)}" fetchpriority="high"><figcaption>{e(p.get('mediaCaption',p['coverAlt']))} <a class="inline-link" href="{cover(p)}" target="_blank" rel="noopener noreferrer">Open full-size figure ↗</a></figcaption></figure>
<div class="case-layout"><aside class="case-sidebar"><nav aria-label="Case study contents">{toc}</nav><div class="sidebar-note mono">{e(p['year'])}<br>{e(p['discipline'])}</div></aside><article class="case-article">{''.join(chapters)}<section class="deliverables"><span class="mono">OUTPUTS &amp; ARTIFACTS</span><ul>{deliverables}</ul></section>{movie}<div class="resource-links">{links}</div></article></div>
<a class="next-project" href="/projects/{next_p['slug']}/"><span class="mono">NEXT STUDY / {next_p['index']}</span><span class="next-title">{e(next_p['title'])}</span><span class="circle-arrow">{arrow()}</span></a></div></main>'''
    return page(p["title"]+" — GXZ",p["summary"],body,"/projects/"+p["slug"]+"/",schema=schema,bodyclass="case-page")

def build(out):
    out.mkdir(parents=True,exist_ok=True)
    if out.resolve()!=ROOT:
        for directory in ["portfolio","fonts","downloads"]:
            if (ROOT/"assets"/directory).exists():shutil.copytree(ROOT/"assets"/directory,out/"assets"/directory,dirs_exist_ok=True)
        for directory,names in {"css":["portfolio.css"],"js":["portfolio.js","motion.js"]}.items():
            (out/"assets"/directory).mkdir(parents=True,exist_ok=True)
            for name in names:shutil.copy2(ROOT/"assets"/directory/name,out/"assets"/directory/name)
    (out/"index.html").write_text(home(),encoding="utf-8")
    for i,p in enumerate(PROJECTS):
        dest=out/"projects"/p["slug"];dest.mkdir(parents=True,exist_ok=True)
        (dest/"index.html").write_text(detail(p,PROJECTS[(i+1)%len(PROJECTS)]),encoding="utf-8")
    (out/"404.html").write_text(page("Page not found — GXZ","Find your way back to GXZ's selected research and experiments.",'<main id="main" tabindex="-1" class="wrap not-found"><span class="mono">404 / OFF THE MAP</span><h1>A different<br>direction.</h1><p>This page may have moved. There is more to explore.</p><a class="hero-cta" href="/"><span>Back to selected work</span><span class="circle-arrow">'+arrow()+'</span></a></main>',"/404.html"),encoding="utf-8")
    redirect='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/#about"><title>About GXZ</title><link rel="canonical" href="https://gxz321.github.io/#about"></head><body><a href="/#about">About GXZ</a></body></html>'
    for name in ["aboutme/index.html","aboutme.html","tags.html"]:
        dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(redirect,encoding="utf-8")
    (out/".nojekyll").write_text("",encoding="utf-8")
    urls=["/"]+["/projects/"+p["slug"]+"/" for p in PROJECTS]
    (out/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f"<url><loc>{SITE}{p}</loc></url>" for p in urls)+'</urlset>',encoding="utf-8")
    (out/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: "+SITE+"/sitemap.xml\n",encoding="utf-8")
    (out/"feed.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>GXZ — Intelligence, in motion.</title><link>'+SITE+'</link><description>Research on people, space, and intelligent systems.</description>'+''.join("<item><title>"+e(p["title"])+"</title><link>"+SITE+"/projects/"+p["slug"]+"/</link><description>"+e(p["summary"])+"</description><guid>"+SITE+"/projects/"+p["slug"]+"/</guid></item>" for p in PROJECTS)+"</channel></rss>",encoding="utf-8")
    print(f"Built {len(PROJECTS)+2} English pages in {out}")

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path,default=ROOT)
    build(parser.parse_args().output.resolve())
