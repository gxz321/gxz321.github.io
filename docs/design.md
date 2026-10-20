# 视觉与实现规范

设计方向：建筑研究式个人作品集。温和纸色 #f5f4f0、正文 #242722、鼠尾草绿 #75816b、少量锈红 #a7462b；细分隔线、开放排版、真实项目媒体。标题使用 Georgia / 中文宋体回退，正文使用系统中文无衬线。桌面内容最大 1440px，48px 边距；手机 20px 边距、单列项目、可展开导航。

概念设计由内置 ImageGen 生成，三张参考分别覆盖首页、项目列表、关于/经历/联系。参考图保存在工作区 `website-research/design/`，不作为网页截图背景使用。

组件：简洁页头、两列首屏、交替项目行、三项研究路径、浅绿联系页脚、项目详情正文与媒体。没有虚构绩效数字、教育身份、装饰统计、无效联系表单。所有正文和控件为可选择 HTML 文本。

与概念的有意差异：用真实 CrowdFlow 与下沉广场图替换生成的媒体槽；GR00T 使用标明进行中的代码原生示意图，不复用未明确授权的上游教程画面；医疗机器人没有虚假的详情按钮；首页增加“概念插画”说明；联系入口使用 GitHub，不发布未经明确授权的邮箱。未提供真实简历前，经历以研究路径呈现。

首页插画生成方式：内置 ImageGen，参考首页设计图。提示词：Create only the standalone isometric plaza illustration from the reference design, no UI, no headline, no lettering, no numbers, no captions, no border. Architectural axonometric line drawing of a generic square sunken public plaza with stairs, glass retaining walls, small trees in sage planting strips, tiny human silhouettes, sparse rust dotted pedestrian routes. Thin precise grey ink lines, muted sage ground, light #f5f4f0 background, same editorial architectural rendering style and view as the reference. Center the entire plaza with generous 3% margins. This is a conceptual spatial illustration, not a representation of any real completed project. 4:3 landscape high quality. Keep reference artwork design consistency, remove all surrounding webpage elements.

最终资产路径：`assets/portfolio/hero-plaza.png`。使用同一内置工具将画外空白移除为透明，保留建筑线稿和植被。编辑提示词：Remove only the plain light beige background outside the architectural drawing to genuine transparency. Preserve the entire architectural isometric plaza illustration, all trees, small people, sparse terracotta pedestrian dotted paths, fine grey linework, pale sage planting beds, stairs and glass retaining walls exactly. The outer canvas must be truly transparent, not beige or gray. Preserve the composition, proportions and original landscape aspect. Keep the original fine lines sharp and the light interior material fills. No new text or objects.

网站不使用外部字体、统计或第三方脚本。
