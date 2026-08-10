---
layout: home
title: GXZ's Lab
subtitle: 技术笔记 × 项目作品
---

Hi，我是 GXZ —— 一个对 **数据、AI 和工程化** 感兴趣的技术人。

这个站点用来记录我的学习轨迹，展示我动手做过的项目。每个项目都尽量做到「可复现、可演示、可面试展示」。

---

## 🧭 导航

- 📝 **[About](aboutme)** — 关于我 & 技能栈
- 🚀 **[Projects](projects)** — 作品集
- 👥 **[CrowdFlow AI](crowdflow-ai)** — 人群安全 AI 规划（主打项目）

---

## 📌 最近更新

{% for post in site.posts limit:3 %}
- **[{{ post.title }}]({{ post.url | relative_url }})** — {{ post.date | date: "%Y-%m-%d" }}
  {{ post.excerpt | strip_html | truncate: 120 }}
{% endfor %}
