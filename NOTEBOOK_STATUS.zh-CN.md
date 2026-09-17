# Notebook 当前状态

更新日期：2026-09-17。

最适合学习者查看的是 Site 的 [Notebook 运行中心](https://ai-beginners-zh-alex.ironman26.chatgpt.site/notebooks.html)。本页说明状态数据如何得出，避免把不同验证范围混为一谈。

## 已确认的运行能力

- 浏览器运行：7 个 JupyterLite 入口已在真实 Chromium 中逐单元验证。[运行记录](https://github.com/azfiles/AI-For-Beginners/actions/runs/35070286053)
- 统一短训练：18 个长训练或兼容性项目完成了真实数据、真实模型路径的缩短运行。[运行记录](https://github.com/azfiles/AI-For-Beginners/actions/runs/35072489957)
- 完整审计：一轮分片审计已经结束并产出发现，长训练超时和修复后项目不会自动标成完整通过。[运行记录](https://github.com/azfiles/AI-For-Beginners/actions/runs/35072071135)

完整审计、短训练、浏览器运行和练习准备代码是四种不同证据。绿色状态只表示状态标签中写明的范围已经通过。

## 需要用户提供条件

| Notebook | 条件 |
| --- | --- |
| `lessons/2-Symbolic/MSConceptGraph.ipynb` | `NEWSAPI_KEY`，或 `NEWS_TITLES_JSON` 本地标题数组；概念查询仍需网络 |
| `lessons/4-ComputerVision/12-Segmentation/SemanticSegmentationPytorch.ipynb` | 登记获取 PH2 数据并设置 `PH2_DATA_DIR` |
| `lessons/4-ComputerVision/12-Segmentation/SemanticSegmentationTF.ipynb` | 登记获取 PH2 数据并设置 `PH2_DATA_DIR` |

PH2 受原始数据条款约束，仓库和 Site 不重新分发。凭据也不会写入 Notebook 或 GitHub Actions。

## 机器可读状态

- `website/notebook-status.json` 保存当前浏览器运行、短训练和受限资源状态；
- `website/validation-status.json` 保存完整审计结果与 Notebook 代码摘要；
- `website/build.py` 只在记录摘要与当前代码一致时显示“完整执行通过”；
- `tools/check_repository_contract.py` 检查这些清单中的文件和浏览器入口仍然存在且互不冲突。

逐文件信息见 [site/VALIDATION.zh-CN.md](site/VALIDATION.zh-CN.md)，环境准备见 [site/RUNNING.zh-CN.md](site/RUNNING.zh-CN.md)。
