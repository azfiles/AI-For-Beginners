# 中文学习站构建与发布

本仓库是中文学习站的源码。GitHub Actions 的 Build Chinese learning site 会检查仓库与站点契约，构建中文讲义、Notebook 阅读页、公式、本地图片和 JupyterLite，并检查站内文件链接。构建产物名为 chinese-learning-site，包含课程静态资源、Worker 服务端和数据库迁移。

构建通过不等于已部署，也不等于全部课程代码通过。浏览器执行、短训练兼容性和完整课程审计由独立工作流检查，失败、超时和受限资源状态不会被隐藏。

运行网站构建需要 Python 3.12、markdown==3.10.3，并将 katex@0.16.22 的 dist 内容放入 website/vendor/katex，保留其 LICENSE；完整命令见 .github/workflows/chinese-site.yml。

执行 `python tools/check_repository_contract.py` 检查声明，再执行 `python website/build.py` 生成 `site-dist/`。随后在 `site-app/` 执行测试和构建，将静态资源、Worker 与迁移组合到 `site-app-dist/`；完整命令以工作流为准。

个人学习界面由 `learning.js` / `learning.css` 提供，服务端实现位于 `site-app/`。生产 Site 使用 ChatGPT 登录提供的用户 ID 和 D1 保存笔记与完成状态；首次连接会自动合并旧版浏览器记录。JSON 导入/导出继续用于备份，短暂同步故障时浏览器只保存待同步副本。

既有 ChatGPT Site 已登记，项目 ID 为 `appgprj_6aa7b84ff31c8191a7e0c4a8b19ac8a0`，已发布：https://ai-beginners-zh-alex.ironman26.chatgpt.site。后续更新复用这一项目；不要新建重复站点。其源仓库推送和发布必须使用 Sites 原生流程，不能将本 GitHub 提交 SHA 冒充 Sites 源仓库的提交。

仓库与部署链路见 `docs/ARCHITECTURE.zh-CN.md`，自动化职责见 `docs/GITHUB_ACTIONS.zh-CN.md`。
