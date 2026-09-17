# AI 入门 · 中文学习站

[![构建中文学习站](https://github.com/azfiles/AI-For-Beginners/actions/workflows/chinese-site.yml/badge.svg)](https://github.com/azfiles/AI-For-Beginners/actions/workflows/chinese-site.yml)
[![浏览器 Notebook](https://github.com/azfiles/AI-For-Beginners/actions/workflows/browser-notebooks.yml/badge.svg)](https://github.com/azfiles/AI-For-Beginners/actions/workflows/browser-notebooks.yml)
[![CodeQL](https://github.com/azfiles/AI-For-Beginners/actions/workflows/codeql.yml/badge.svg)](https://github.com/azfiles/AI-For-Beginners/actions/workflows/codeql.yml)

这是 [Microsoft AI for Beginners](https://github.com/microsoft/AI-For-Beginners) 的中文学习与运行版本。仓库以中文 Site 为主要产品，不再追求与原仓库的目录说明、首页或自动化风格一致；上游课程内容仍保留来源和许可证说明。

## 从这里开始

- [打开中文学习站](https://ai-beginners-zh-alex.ironman26.chatgpt.site/)
- [进入 Notebook 运行中心](https://ai-beginners-zh-alex.ironman26.chatgpt.site/notebooks.html)
- [查看运行环境说明](site/RUNNING.zh-CN.md)
- [查看逐项验证状态](site/VALIDATION.zh-CN.md)

站点中的 Notebook 入口分为两类：蓝色「浏览器运行」在 JupyterLite/Pyodide 中直接执行；白色「下载 .ipynb」用于本机 Jupyter、Docker 或其他完整 Python 环境。TensorFlow、PyTorch、需要本地数据或凭据的课程不会伪装成浏览器可运行。

## 当前能力

| 方式 | 适合内容 | 当前状态 |
| --- | --- | --- |
| Site 浏览器运行 | 纯 Python、NumPy、scikit-learn、部分符号推理课程 | 7 个入口已在真实 Chromium 中逐单元验证 |
| 本机 Docker/Jupyter | TensorFlow、PyTorch、长训练、模型和本地数据 | 提供固定版本环境与持久化缓存 |
| 下载 Notebook | 自行选择 Colab、本机或其他 Jupyter 环境 | 所有 Notebook 均保留原文件下载入口 |

状态标记不是装饰：绿色表示对应代码哈希已有完整或明确范围的短训练证据；黄色表示仍需完整复验；红色表示缺少凭据、受限数据或外部服务。当前受限项包括 Microsoft Concept Graph 的新闻/API 输入，以及两份需要 PH2 数据集的语义分割 Notebook。

## 本机快速启动

推荐使用仓库提供的 Docker 环境：

```bash
docker compose -f runtime/compose.yaml up --build
```

随后按终端输出的带 token 地址打开 JupyterLab。详细的 CPU 平台、数据目录、模型缓存和不使用 Docker 的安装方法见 [runtime/README.zh-CN.md](runtime/README.zh-CN.md)。

构建中文 Site：

```bash
python -m pip install markdown==3.10.3
python website/build.py
```

完整的 JupyterLite 和 KaTeX 构建步骤以 [.github/workflows/chinese-site.yml](.github/workflows/chinese-site.yml) 为准。输出目录为 `site-dist/`。

## 仓库结构

| 目录 | 用途 |
| --- | --- |
| `translations/zh-CN/` | 中文课程正文 |
| `lessons/`、`examples/` | Notebook、脚本、图片与课程资源 |
| `website/` | 中文 Site 生成器、样式、JupyterLite 配置和状态数据 |
| `site/` | 面向学习者的运行及验证说明 |
| `runtime/` | Docker/Jupyter 完整 Python 环境 |
| `tools/` | Notebook 审计、浏览器测试与仓库契约检查 |
| `.github/workflows/` | 构建、安全扫描和分层 Notebook 验证 |

站点生成与验证数据之间的关系见 [docs/ARCHITECTURE.zh-CN.md](docs/ARCHITECTURE.zh-CN.md)，每个 GitHub Action 的职责见 [docs/GITHUB_ACTIONS.zh-CN.md](docs/GITHUB_ACTIONS.zh-CN.md)。

## 验证口径

“Site 构建成功”只代表页面与资源可以生成，不代表所有训练都已完成。“短训练通过”表示保留真实数据和真实模型路径，但缩短批次、轮数或优化步数；它不等于原规模训练效果验收。练习 Notebook 的准备代码通过，也不代表题目答案已填写。

机器可读状态位于：

- `website/notebook-status.json`：浏览器、短训练、凭据和受限数据状态；
- `website/validation-status.json`：完整审计结果与代码摘要；
- `validation/results.json`：审计工作流产物中的逐项原始结果（不作为固定源码提交）。

## 上游与许可

课程内容源自 [microsoft/AI-For-Beginners](https://github.com/microsoft/AI-For-Beginners)。本仓库对中文导航、运行环境、Notebook 兼容性、验证和部署进行了独立改造，不代表 Microsoft 官方发布。同步上游时采用选择性合并，不会覆盖本仓库的运行修复和中文站点结构。

项目继续遵循仓库中的 [MIT License](LICENSE)。课程图片、数据集和外部模型还可能受各自来源条款约束。
