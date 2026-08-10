---
layout: page
title: CrowdFlow AI
subtitle: AI-Assisted Crowd Planning for Large Events
share-title: "CrowdFlow AI | AI-Powered Crowd Safety"
---

> Social Force Model + LLM crowd planning tool  
> Validated with real CCTV data from the 2022 Lyon Festival of Lights

---

## 📖 Background

December 2022 — Place des Terreaux, Lyon, France. The Fête des Lumières (Festival of Lights).

CCTV tracked **11,904 people** moving through a ~60m × 70m plaza:

| Data Point | Value | Significance |
|------------|-------|-------------|
| 🎯 People Tracked | 11,904 | CCTV trajectory data |
| ⚡ Contact Events | 446 | Recorded by 16 sensor-wearing volunteers |
| 🐌 Lowest Mean Speed | **0.04 m/s** | Near-complete standstill |
| 😰 Highest Individual Contacts | **99 / 20 min** | Extreme crowding |

> *"Could AI-assisted planning have prevented this?"*

![CrowdFlow AI Dashboard](/assets/img/crowdflow-preview.png)

---

## 🧠 Architecture

| Layer | Technology | Role |
|-------|-----------|------|
| **Data** | Real CCTV trajectory data | Ground truth |
| **Simulation** | Social Force Model (Helbing & Molnár, 1995) | Pedestrian movement under any layout |
| **AI Analysis** | LLM (GPT-4o / Ollama local) | Diagnose bottlenecks, generate recommendations |
| **Visualization** | Streamlit + Matplotlib + Canvas animation | Interactive dashboard |

---

## 🎯 What the AI Changed

The core decision: **asymmetric gate-width distribution**

```
Human Plan (equal-width)        AI Recommended (behavior-compensating)
        
  Gate1  Gate2  Gate3        Gate1  Gate2  Gate3
  ┌────┐┌────┐┌────┐        ┌──┐ ┌──────┐ ┌──┐
  │2.0m││2.0m││2.0m│        │1.5│ │3.5m  │ │1.5│
  └────┘└────┘└────┘        └──┘ └──────┘ └──┘
    33%   33%   33%            22%   55%    22%  ← width allocation
                              ↑_____↑_____↑
  Actual flow: 22%  55%  22%  Actual flow: 30%  40%  30%  ← more balanced
```

### The AI's Insight

People naturally take the shortest path, putting ~55% of pressure on the center gate.
Equal-width design fails to compensate for this behavioral bias.
**AI uses asymmetric design to counteract irrational human behavior.**

### Three-Tier Recommendations

| Priority | Recommendation | Rationale |
|----------|---------------|-----------|
| 🔴 High | Center gate 3.5m, sides 1.5m | Width compensates for behavioral bias |
| 🟡 Medium | Flare barriers outward 15° | +30% queue area, natural flow diversion |
| 🟢 Low | Extend barriers to 5m + floor guide lines | Low-cost buffer expansion |

### Expected Impact

| Metric | Equal-Width | AI-Optimized | Improvement |
|--------|-------------|-------------|-------------|
| Pass Rate | ~40% | ~75% | ↑88% |
| Peak Density | 3.5+ ppl/m² | <2 ppl/m² | ↓43% |
| Collisions | 120+ | <60 | ↓50% |
| Center Gate Load | ~55% | ~40% | Balanced |

---

## 🏗️ Simulation Scene

The dashboard models a **36m × 24m** medium-scale festival entrance:

```
      ← Queue barriers ← Security gates → Event zone →
      
         🚧 Gate 1 (1.5m) 🚧
      Queue buffer          🏃→
         🚧 Gate 2 (3.5m) 🚧   ← AI-widened
      (forecourt)           🏃→
         🚧 Gate 3 (1.5m) 🚧
                            🏃→
```

Tunable: visitors (60–240) · barrier length (2–6m) · simulation steps (100–500)

---

## 🚀 Try It

- **▶️ [Live Demo](https://crowdflows-ai-gk8xsndjykcrgvtyk3wfbm.streamlit.app)**
- **📂 [GitHub Repo](https://github.com/gxz321/crowdflows-ai)**

### Run Locally

```bash
git clone https://github.com/gxz321/crowdflows-ai.git
cd crowdflows-ai
python -m venv .venv
.venv\Scripts\activate  # or `source .venv/bin/activate` on macOS/Linux
pip install -r crowdflow_ai/requirements.txt
streamlit run crowdflow_ai/app.py
```

---

## 🛠 Tech Stack

- **Simulation**: PyTorch · socialforce · Social Force Model
- **Data**: pandas · scipy · shapely · pyproj
- **AI**: OpenAI API / Ollama (LLM Agent)
- **UI**: Streamlit · Matplotlib · Canvas animation
- **Design**: CSS variable system · dark theme · Glacier Blue palette

---

## 📝 Related Writing

Coming soon — a technical deep-dive on applying Social Force Models to crowd planning.

---

## 📬 Feedback

Issues and PRs welcome! Contact: [GitHub @gxz321](https://github.com/gxz321)
