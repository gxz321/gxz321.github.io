---
layout: page
title: Projects
subtitle: 动手做过的项目
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

## 🚧 规划中

- 🧊 冰蓝极简设计系统（CSS 变量体系）
- 📊 里昂灯光节数据深度分析
- 🐳 Docker 容器化部署方案
