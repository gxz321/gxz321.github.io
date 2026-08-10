---
layout: page
title: Projects
subtitle: Things I've built
---

{% for project in site.data.projects %}

## {{ project.name }}

{{ project.description }}

{% if project.links %}
{% for link in project.links %}
- [{{ link.name }}]({{ link.url }}){:target="_blank"}
{% endfor %}
{% endif %}

{% endfor %}

---

## 🚧 In the Pipeline

- 🧊 Glacier Blue design system (CSS variable architecture)
- 📊 Deep-dive analysis of Lyon Festival of Lights data
- 🐳 Docker containerization for deployment
