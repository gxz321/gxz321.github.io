---
layout: page
title: CrowdFlow AI
subtitle: AI-Assisted Crowd Planning for Large Events
share-title: "CrowdFlow AI | 人群安全 AI 规划"
---

> 基于社会力模型 + LLM 的大型活动人群规划工具  
> 使用 2022 年里昂灯光节真实 CCTV 数据验证

---

## 📖 项目背景

2022 年 12 月，法国里昂 Place des Terreaux 举办灯光节（Fête des Lumières）。

CCTV 追踪了 **11,904 人** 在约 60m×70m 的广场中的移动：

| 数据点 | 数值 | 含义 |
|--------|------|------|
| 🎯 追踪人数 | 11,904 | CCTV 轨迹数据 |
| ⚡ 碰撞事件 | 446 次 | 16 名志愿者佩戴传感器记录 |
| 🐌 最低均速 | **0.04 m/s** | 几乎完全停滞 |
| 😰 最高单人碰撞 | **99 次 / 20 分钟** | 极端拥挤状况 |

> *"如果 AI 参与了规划，是否能避免这些？"*

![CrowdFlow AI Dashboard](/assets/img/crowdflow-preview.png)

---

## 🧠 技术架构

| 层级 | 技术 | 作用 |
|------|------|------|
| **数据层** | 真实 CCTV 轨迹数据 | 提供 Ground Truth |
| **模拟引擎** | Social Force Model (Helbing & Molnár, 1995) | 模拟任意布局下的人群移动 |
| **AI 分析** | LLM (GPT-4o / Ollama 本地模型) | 诊断瓶颈、生成优化建议 |
| **可视化** | Streamlit + Matplotlib + Canvas 动画 | 交互式仪表盘 |

---

## 🎯 AI 改了什么

核心决策：**非对称闸门宽度分配**

```
人类方案（等宽思维）          AI 推荐（行为补偿）
        
  Gate1  Gate2  Gate3        Gate1  Gate2  Gate3
  ┌────┐┌────┐┌────┐        ┌──┐ ┌──────┐ ┌──┐
  │2.0m││2.0m││2.0m│        │1.5│ │3.5m  │ │1.5│
  └────┘└────┘└────┘        └──┘ └──────┘ └──┘
    33%   33%   33%            22%   55%    22%  ← 宽度分配
                              ↑_____↑_____↑
    实际流量: 22%  55%  22%   实际流量: 30%  40%  30%  ← 更均衡
```

### AI 的洞察

人群天然选择最短路径，导致中间闸门承受 ~55% 的压力。
等宽设计没有补偿这种行为偏差。
**AI 通过非对称设计对冲人类的非理性行为**。

### 三层建议

| 优先级 | 建议 | 原理 |
|--------|------|------|
| 🔴 高 | 中间闸门 3.5m，两侧 1.5m | 宽度补偿行为偏差 |
| 🟡 中 | 护栏外扩 15° 喇叭口 | 排队区 +30%，自然引导分流 |
| 🟢 低 | 延伸护栏至 5m + 地面视觉线 | 低成本增加缓冲 |

### 预期效果

| 指标 | 等宽设计 | AI 优化 | 改善 |
|------|---------|---------|------|
| 通过率 | ~40% | ~75% | ↑88% |
| 峰值密度 | 3.5+ 人/m² | <2 人/m² | ↓43% |
| 碰撞次数 | 120+ | <60 | ↓50% |
| 中间闸门负载 | ~55% | ~40% | 均衡化 |

---

## 🏗️ 模拟场景

Dashboard 模拟一个 **36m × 24m** 的中型音乐节入场口：

```
      ← 排队护栏 ← 安检闸门 → 活动区域 →
      
         🚧 Gate 1 (1.5m) 🚧
      排队缓冲区        🏃→
         🚧 Gate 2 (3.5m) 🚧   ← AI 拓宽
       (forecourt)      🏃→
         🚧 Gate 3 (1.5m) 🚧
                        🏃→
```

可调参数：访客数 (60–240) · 护栏长度 (2–6m) · 模拟步数 (100–500)

---

## 🚀 在线体验

- **▶️ [Streamlit Demo](https://crowdflow-ai.streamlit.app)**（待部署）
- **📂 [GitHub 仓库](https://github.com/gxz321/crowdflow-ai)**

### 本地运行

```bash
git clone https://github.com/gxz321/crowdflow-ai.git
cd crowdflow-ai
python -m venv .venv
.venv\Scripts\activate
pip install -r crowdflow_ai/requirements.txt
streamlit run crowdflow_ai/app.py
```

---

## 🛠 技术栈

- **模拟**: PyTorch · socialforce · Social Force Model
- **数据**: pandas · scipy · shapely · pyproj
- **AI**: OpenAI API / Ollama (LLM Agent)
- **界面**: Streamlit · Matplotlib · Canvas 动画
- **设计**: CSS 变量体系 · 暗色主题 · Glacier Blue 配色

---

## 📝 相关文章

暂无。计划写一篇关于「社会力模型在人群规划中的应用」的技术笔记。

---

## 📬 反馈

欢迎提 Issue 或 PR！联系：[GitHub @gxz321](https://github.com/gxz321)
