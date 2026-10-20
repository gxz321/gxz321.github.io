# 项目内容来源与展示边界

核查日期：2026-10-20。网站项目内容维护于 `content/projects.json`。本说明只记录来源、素材与完成状态，不收集个人身份或联系方式。

## CrowdFlow AI

内容依据工作区 `Cambridge crowdflow ai/` 中的 `README.md`、`crowdflow_ai/app.py`、`simulator.py`、`llm_agent.py`、`data_story.py`、`spatial_story.py` 和数据文件。源码地址通过本地 Git remote 核实：[gxz321/crowdflows-ai](https://github.com/gxz321/crowdflows-ai)。[演示链接](https://crowdflows-ai-gk8xsndjykcrgvtyk3wfbm.streamlit.app)来自既有项目页面，当前在线运行状态尚未验证。

素材映射：

- `assets/portfolio/crowdflow.png`：原项目 `crowdflow_ai/ppt_build/visuals/flow-field-crop.png`，为人流方向分析图，原样复制。
- `assets/portfolio/crowdflow-simulation.png`：原项目 `crowdflow_ai/ppt_build/visuals/simulation-before-gate.png`，为探索性仿真图。

原项目使用里昂灯光节 CCTV 轨迹与接触数据。本站将它们标为数据分析与仿真材料，不表示这些现场数据由网站作者采集。正式再分发数据前应继续核对原始数据许可。

状态为“研究原型”。当前页面不使用预置 LLM 回复中的改善百分比，不将预设布局对比称为自动求得最优方案。导出轨迹存在待校正的解析口径，暂不展示“11,904 人”和未经重新核实的速度结论。模拟潜在接触与观测接触事件属于不同指标。未发现现场干预或独立校准验证记录。

## 下沉广场

内容依据 `下沉广场研究文件/空间汇报(2)(2).pptx`、现场照片，以及 Rhino / Grasshopper 文件；核查记录见工作区 `website-research/sunken.md`。2025 年口径由文件元数据和采样影像时间共同支持。

素材从原汇报提取后原样复制：

- `assets/portfolio/sunken.png`：PPT 媒体 `image13.png`，三维场景与人流可视化。
- `assets/portfolio/sunken-site.png`：PPT 媒体 `image22.png`，广场现场总览。
- `assets/portfolio/sunken-flow.mp4`：PPT 媒体 `media6.mp4`，第 14 页的人流动画。

这些材料来自课程小组研究。网站不将全部采集、建模或分析归为个人独立成果；未使用团队人像、学生信息或院校标志作为个人品牌。涉及地图或卫星底图时保留原有归属信息。

状态为“课程研究 · 可视化原型”。现有观察只覆盖采样时段，路径与设施建议属于研究讨论，不表示已经实施改造、验证因果或建成连续运行的数字孪生系统。

## GR00T 仿真训练

起点是工作区 `GR00T/Isaac-Sim-with-Gr00t-Tutorial-main.zip`，其 README 与公开[上游教程](https://github.com/donghoYee/Isaac-Sim-with-Gr00t-Tutorial)相符。模型与工具资料参考 [NVIDIA Isaac GR00T](https://github.com/NVIDIA/Isaac-GR00T)。上游教程面向 N1.5；官方主分支会继续更新，后续实验应固定兼容的软件、模型和资产版本。

`assets/portfolio/groot.svg` 是为本站绘制的代码原生流程图，表示数据准备、策略服务与仿真接入关系，不是机器人实测画面。未使用第三方教程的视频或截图充作个人项目成果。

状态为“工程完善中”。准备检查、协议测试、模拟响应和启动脚本只说明工程准备进展；真实 GPU 训练、模型推理与 Isaac Sim 闭环评估尚待完成。后续成果需附配置、日志、任务视频与实验记录。本站未声明已经取得任务成功率、闭环成功或机器人实机部署成果。

## 医疗机器人

按项目主人要求保留待补充入口。代码、完整包与可公开材料提供后，再核对方法、贡献和结果；当前不生成项目技术或临床成效描述。
