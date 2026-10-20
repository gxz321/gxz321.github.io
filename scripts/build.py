"""Build a dependency-free, pre-rendered portfolio for GitHub Pages."""
from pathlib import Path
import argparse
import html
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
e = html.escape
PROFILE = json.loads((ROOT / 'content/profile.json').read_text(encoding='utf-8'))
PROJECTS = json.loads((ROOT / 'content/projects.json').read_text(encoding='utf-8'))
SITE = 'https://gxz321.github.io'

def nav():
    return '''<a class="skip-link" href="#main">跳到主要内容</a>
<header class="site-header container"><a class="brand" href="/" aria-label="GXZ 首页"><strong>GXZ.</strong><span>projects &amp; experiments</span></a>
<button class="menu-toggle" aria-expanded="false" aria-controls="main-nav">菜单 ＋</button>
<nav class="main-nav" id="main-nav" aria-label="主导航"><a href="/#projects">项目</a><a href="/#journey">经历</a><a href="/#about">关于</a><a href="/#contact">联系</a><a class="nav-github" href="https://github.com/gxz321" target="_blank" rel="noopener noreferrer">GitHub ↗</a></nav></header>'''

def footer():
    return f'''<footer id="contact" class="contact-band"><div class="container contact-inner"><h2>一起讨论下一个想法。</h2><div class="contact-links"><div><a href="https://github.com/gxz321" target="_blank" rel="noopener noreferrer">联系我 ↗</a><a href="https://github.com/gxz321?tab=repositories" target="_blank" rel="noopener noreferrer">浏览代码 ↗</a></div><p>© 2026 {e(PROFILE['name'])} / Built with curiosity.</p></div></div></footer>'''

def page(title, description, body, path='/', image='/assets/portfolio/hero-plaza.png', schema=None):
    structured = json.dumps(schema or {'@context':'https://schema.org','@type':'WebSite','name':'GXZ · 项目与研究','url':SITE}, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f5f4f0"><title>{e(title)}</title><meta name="description" content="{e(description,quote=True)}"><link rel="canonical" href="{SITE}{path}"><meta property="og:type" content="website"><meta property="og:locale" content="zh_CN"><meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(description,quote=True)}"><meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{SITE}{image}"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/svg+xml" href="/assets/portfolio/favicon.svg"><link rel="stylesheet" href="/assets/css/portfolio.css"><script src="/assets/js/portfolio.js" defer></script><script type="application/ld+json">{structured}</script></head><body>{nav()}{body}{footer()}</body></html>'''

def project_row(p, reverse=False):
    return f'''<article class="project-row{' reverse' if reverse else ''}"><a class="project-media" href="/projects/{p['slug']}/" aria-label="查看 {e(p['title'],quote=True)} 项目"><img src="{p['cover']}" alt="{e(p['coverAlt'],quote=True)}" width="1000" height="620" loading="lazy"></a><div class="project-info"><div class="project-category"><span>{p['index']}</span>/ &nbsp; {e(p['category'])}</div><h3><a href="/projects/{p['slug']}/">{e(p['title'])}</a></h3><p>{e(p.get('short',p['summary']))}</p><div class="project-meta"><span>{e(p['status'])}</span><span>{e(' · '.join(p['stack'][:3]))}</span></div><a class="project-link" href="/projects/{p['slug']}/">查看项目 <span aria-hidden="true">↗</span></a></div></article>'''

def home():
    rows = ''.join(project_row(p, i % 2 == 1) for i, p in enumerate(PROJECTS))
    body = f'''<main id="main" class="container"><section class="hero" aria-labelledby="hero-heading"><div class="hero-copy"><h1 id="hero-heading">在真实问题中，<span>探索智能与空间。</span></h1><p class="hero-description">我关注人群流动、机器人仿真与空间设计，<br>把观察转化为模型，把想法推进到实验。</p><div class="hero-actions"><a class="button" href="#projects">浏览项目 <span aria-hidden="true">↘</span></a><a class="text-link" href="#about">了解我 <span aria-hidden="true">→</span></a></div></div><figure class="hero-figure"><img src="/assets/portfolio/hero-plaza.png" width="1448" height="1086" alt="下沉公共空间与步行路径的建筑轴测概念插画" fetchpriority="high"><figcaption>空间 × 感知 × 行动 · 概念插画</figcaption></figure><a class="scroll-cue" href="#projects" aria-label="向下浏览项目">↓</a></section>
<section id="projects" aria-labelledby="projects-heading"><div class="section-heading"><h2 id="projects-heading">精选项目</h2><p>Selected work <span>01 — 04</span></p></div>{rows}<article class="project-row reverse pending"><div class="project-media pending-media" role="img" aria-label="医疗机器人项目内容待补充"><span>To be continued.</span></div><div class="project-info"><div class="project-category"><span>04</span>/ &nbsp; ROBOTICS</div><h3>医疗机器人</h3><p>资料整理中，项目详情后续更新。</p><div class="project-meta"><span>待补充程序代码与完整项目包</span></div></div></article></section>
<section class="about" id="about" aria-labelledby="about-heading"><div class="about-heading"><h2 id="about-heading">关于我</h2><span>About</span></div><div class="about-copy"><p class="about-statement">在代码与空间之间，<br>持续学习，动手验证。</p><p>我关注智能系统如何感知环境、理解人的行为，并在真实问题中发挥作用。这里记录我的项目、研究过程与尚在推进的实验。</p></div></section>
<section class="journey" id="journey" aria-labelledby="journey-heading"><div class="journey-heading"><h2 id="journey-heading">探索路径</h2><span>/ Research journey</span></div><a class="journey-row" href="/projects/crowdflow-ai/"><strong>人群流动</strong><p>轨迹数据、拥堵分析与可视化</p><span aria-hidden="true">→</span></a><a class="journey-row" href="/projects/sunken-plaza/"><strong>空间研究</strong><p>下沉广场、步行体验与空间形态</p><span aria-hidden="true">→</span></a><a class="journey-row" href="/projects/groot/"><strong>机器人学习</strong><p>Isaac Sim、仿真数据与 GR00T</p><span aria-hidden="true">→</span></a></section></main>'''
    return page('GXZ · 项目与研究', 'GXZ 的个人作品集：CrowdFlow AI 人群流动分析、下沉广场空间研究、GR00T 与 Isaac Sim 仿真学习，以及持续推进的机器人项目。', body)

def detail(p, next_p):
    sections = ''.join(f'''<section class="detail-section"><h2>{e(s['title'])}</h2>{''.join('<p>'+e(t)+'</p>' for t in s['paragraphs'])}</section>''' for s in p['sections'])
    links = ''.join(f'<a href="{e(l["url"],quote=True)}" '+('download' if l['url'].endswith('.zip') else 'target="_blank" rel="noopener noreferrer"')+f'>{e(l["label"])} ↗</a>' for l in p['links'])
    gallery = ''
    if p['slug'] == 'crowdflow-ai':
        gallery = '<figure><img src="/assets/portfolio/crowdflow-simulation.png" loading="lazy" alt="社会力入口仿真示例，展示行人位置与闸门布局"><figcaption>已有社会力仿真画面。单次模拟仅用于探索，不代表实际干预效果。</figcaption></figure>'
    if p['slug'] == 'sunken-plaza':
        gallery = '''<figure><img src="/assets/portfolio/sunken-site.png" loading="lazy" alt="同济大学校园下沉广场的日间固定机位研究画面"><figcaption>现场采样：观察通行、停留与空间使用。</figcaption></figure><figure><video controls preload="none" playsinline poster="/assets/portfolio/sunken.png" aria-label="Rhino 中的人流空间可视化动画"><source src="/assets/portfolio/sunken-flow.mp4" type="video/mp4">浏览器不支持视频。<a href="/assets/portfolio/sunken-flow.mp4">下载查看动画</a></video><figcaption>原课程汇报中的 Rhino 人流动画，基于采集时段的探索性复现。</figcaption></figure>'''
    download = ''
    schema = {'@context':'https://schema.org','@type':'CreativeWork','name':p['title'],'description':p['summary'],'url':SITE+'/projects/'+p['slug']+'/', 'creativeWorkStatus':p['status']}
    body = f'''<main id="main" class="container detail-main"><a class="back-link" href="/#projects">← 返回精选项目</a><header class="detail-header"><div class="project-category"><span>{p['index']}</span>/ &nbsp; {e(p['category'])}</div><h1>{e(p['title'])}</h1><p class="english-title">{e(p['englishTitle'])}</p><p class="detail-lead">{e(p['summary'])}</p><div class="detail-meta"><span>{e(p['year'])}</span><span>{e(p['status'])}</span><span>{e(' · '.join(p['stack']))}</span></div></header><figure class="detail-cover"><img src="{p['cover']}" width="1000" height="620" alt="{e(p['coverAlt'],quote=True)}"><figcaption>{e(p['coverAlt'])}</figcaption></figure><div class="detail-content">{sections}<div class="detail-links">{links}{download}</div><div class="detail-gallery">{gallery}</div><nav class="project-next" aria-label="项目导航"><a href="/#projects">← 全部项目</a><a href="/projects/{next_p['slug']}/">{e(next_p['title'])} →</a></nav></div></main>'''
    return page(p['title']+' · GXZ', p['summary'],body,'/projects/'+p['slug']+'/',p['cover'],schema)

def build(out):
    out.mkdir(parents=True, exist_ok=True)
    if out.resolve() != ROOT:
        shutil.copytree(ROOT/'assets/portfolio',out/'assets/portfolio',dirs_exist_ok=True)
        for folder, name in [('css','portfolio.css'),('js','portfolio.js')]:
            (out/'assets'/folder).mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/'assets'/folder/name,out/'assets'/folder/name)
        if (ROOT/'assets/downloads').exists():
            shutil.copytree(ROOT/'assets/downloads',out/'assets/downloads',dirs_exist_ok=True)
    (out/'index.html').write_text(home(),encoding='utf-8')
    for i,p in enumerate(PROJECTS):
        dest=out/'projects'/p['slug'];dest.mkdir(parents=True,exist_ok=True)
        (dest/'index.html').write_text(detail(p,PROJECTS[(i+1)%len(PROJECTS)]),encoding='utf-8')
    (out/'404.html').write_text(page('页面未找到 · GXZ','返回 GXZ 的项目与研究首页。','<main id="main" class="container empty-state"><h1>404 / 迷路了。</h1><p>这个页面可能已更新，继续探索项目与研究。</p><a class="button" href="/">返回首页 ↗</a></main>','/404.html'),encoding='utf-8')
    redirect='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/#about"><title>关于 GXZ</title><link rel="canonical" href="https://gxz321.github.io/#about"></head><body><a href="/#about">查看关于我</a></body></html>'
    for path in ['aboutme/index.html','aboutme.html','tags.html']:
        dest=out/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(redirect,encoding='utf-8')
    (out/'.nojekyll').write_text('',encoding='utf-8')
    urls=['/']+['/projects/'+p['slug']+'/' for p in PROJECTS]
    (out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{SITE}{p}</loc></url>' for p in urls)+'</urlset>',encoding='utf-8')
    (out/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+SITE+'/sitemap.xml\n',encoding='utf-8')
    (out/'feed.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>GXZ · 项目与研究</title><link>'+SITE+'</link><description>人群流动、空间研究与机器人仿真。</description>'+''.join('<item><title>'+e(p['title'])+'</title><link>'+SITE+'/projects/'+p['slug']+'/</link><description>'+e(p['summary'])+'</description><guid>'+SITE+'/projects/'+p['slug']+'/</guid></item>' for p in PROJECTS)+'</channel></rss>',encoding='utf-8')
    print(f'Built {len(PROJECTS)+2} pages in {out}')

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT);args=parser.parse_args();build(args.output.resolve())
