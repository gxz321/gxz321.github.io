---
layout: home
title: GXZ's Lab
subtitle: Tech Notes × Project Portfolio
---

Hi, I'm GXZ — a technologist passionate about **data, AI, and engineering**.

This site documents my learning journey and showcases hands-on projects. Every project aims to be reproducible, demonstrable, and interview-ready.

---

## 🧭 Navigate

- 📝 **[About](aboutme)** — About me & skills
- 🚀 **[Projects](projects)** — Portfolio
- 👥 **[CrowdFlow AI](crowdflow-ai)** — AI-powered crowd safety (flagship)

---

## 📌 Recent Posts

{% for post in site.posts limit:3 %}
- **[{{ post.title }}]({{ post.url | relative_url }})** — {{ post.date | date: "%Y-%m-%d" }}
  {{ post.excerpt | strip_html | truncate: 120 }}
{% endfor %}
