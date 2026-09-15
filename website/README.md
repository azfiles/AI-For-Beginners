# 中文学习站构建与恢复

源码已保存到本仓库。GitHub Actions 的 Build Chinese learning site 会构建中文讲义、Notebook 阅读页、公式和本地图片，并检查站内文件链接。构建产物名为 chinese-learning-site。

构建通过不等于已部署，也不等于全部课程代码通过。课程执行由独立的 Chinese curriculum execution audit 工作流检查，失败不会被隐藏。

运行网站构建需要 Python 3.12、markdown==3.10.3，并将 katex@0.16.22 的 dist 内容放入 website/vendor/katex，保留其 LICENSE；完整命令见 .github/workflows/chinese-site.yml。

执行 python website/build.py，输出到 site-dist。当前构建使用根路径，部署目标应以站点根目录提供 index.html，不能直接放在未配置前缀的子路径下。

既有 ChatGPT Site 已登记，项目 ID 为 appgprj_6aa7b84ff31c8191a7e0c4a8b19ac8a0，已发布：https://ai-beginners-zh-alex.ironman26.chatgpt.site。后续更新复用这一项目；不要新建重复站点。其源仓库推送和发布必须使用 Sites 原生流程，不能将本 GitHub 提交 SHA 冒充 Sites 源仓库的提交。
