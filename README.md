# GXZ · 项目与研究

个人作品集，面向 GitHub Pages：CrowdFlow AI、下沉广场、GR00T × Isaac Sim。医疗机器人按计划保留为待补充项目。

网站使用静态 HTML、CSS 和少量原生 JavaScript，没有运行时依赖；正文预先生成，关闭 JavaScript 仍能浏览项目。

## 编辑与预览

1. 修改 `content/projects.json` 的项目内容和 `content/profile.json` 的署名。联系入口使用 GitHub。
2. 将自己的项目图放入 `assets/portfolio/`，更新项目的 `cover` 与 `coverAlt`。
3. 运行 `python scripts/build.py` 生成仓库根目录的网页。
4. 运行 `python scripts/check_site.py` 检查内部链接、图片、元数据和页面结构。
5. 运行 `python -m http.server 8080 --bind 127.0.0.1`，浏览 `http://127.0.0.1:8080/`。

独立部署目录可用 `python scripts/build.py --output dist` 构建。发布到现有 GitHub Pages 仓库时，使用 `master / (root)`，保留 `.nojekyll`。`dist/` 是生成文件，不需要提交。

## 内容维护

- 医疗机器人项目未导入或推断任何未提供的代码。补充资料后，再添加内容和详情页。
- “探索路径”呈现项目经历，不虚构学历、任职或未经确认的个人分工。
- 项目状态和限制写在各自详情页。GR00T 的真实训练与仿真验证仍需数据、模型权重及相应 GPU 环境。
- 来源与图片归属见 `docs/content-sources.md`。首页插画为 AI 生成的空间概念图，不是项目成果或场地实景。
- 项目视觉规范见 `docs/design.md`。旧 Jekyll 主题源保留在仓库中供追溯，当前网站直接使用静态页面。原主题 MIT 许可继续保留。

新页面生成后应一并提交 HTML 与内容源，避免 GitHub Pages 发布旧页面。
