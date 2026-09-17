# GitHub Actions 说明

本仓库把“能生成网站”“能在浏览器执行”“能短训练”和“能完整执行”拆成不同工作流。这样某一层通过时，不会掩盖另一层的问题。

| 工作流 | 作用 | 成功代表什么 |
| --- | --- | --- |
| Build Chinese learning site | 构建中文页面、JupyterLite、公式和本地资源，检查链接并上传 `chinese-learning-site` | 可生成可部署的静态站点 |
| Browser notebook execution | 在真实 Chromium/JupyterLite 中逐单元运行浏览器白名单 | 这些入口可在浏览器执行 |
| Chinese curriculum execution audit | 以真实 Jupyter 内核分片执行课程，保留逐项报告 | 获得完整审计证据；单项失败或超时仍会记录 |
| Read curriculum execution report | 汇总审计产物，便于人工阅读和更新状态 | 报告可读，不等于失败项已修复 |
| Long notebook all-cell compatibility | 对长训练 Notebook 使用明确缩短参数执行所有单元 | 真实路径短训练兼容，不等于原规模训练完成 |
| Autoencoders / Generative / NLP smoke | 针对高风险课程做窄范围真实训练回归 | 对应模型路径未回归 |
| Transfer fine-tuning / symbolic / resource notebooks | 验证微调、符号推理、外部资源加载等专项路径 | 对应专项条件通过 |
| Resource check | 校验课程引用的本地资源、数据路径和下载策略 | 资源约定没有明显断裂 |
| Local notebook runtime | 构建 Docker 环境并检查 Jupyter、框架导入及鉴权 | 本机运行入口可启动且基础依赖可用 |
| Export course sources | 打包课程源码，供下载或发布流程使用 | 源文件可以稳定导出 |
| CodeQL | 静态安全分析 | 未发现阻断级代码扫描问题 |
| Scorecard | 检查仓库供应链与安全实践 | 获得安全基线信号，不是功能测试 |

工作流文件名可能继续按历史用途保留；以其中的 `name:` 和实际步骤为准。仓库首页只展示最直接影响学习者的构建、浏览器运行和安全状态。

## 触发策略

默认分层如下：

- PR/受影响目录自动运行：中文 Site 构建、浏览器 Notebook、Autoencoders/GAN/NLP/Symbolic 等短测，以及 CodeQL；
- 仅手动运行：原始数据下载、资源 Notebook、全量课程审计、长 Notebook 兼容性、DeepRL/其他高耗时修复复验、本机运行时和源码导出；
- 审计报告：只在手动启动的 `Chinese curriculum execution audit` 完成后由 `workflow_run` 自动读取；
- Scorecard：只在 `main` 有 push 时运行，不设 schedule；
- Dependabot：由 GitHub 自身机制管理，不属于 Notebook Actions。

这样普通 PR 只承担快速合并所需的反馈；需要大量下载、长时间训练或全量覆盖时，在 Actions 页面手动启动对应任务即可。

## 如何解读失败

- Site 构建失败：不能发布本次站点版本，应先修复页面、资源或契约问题。
- 浏览器执行失败：对应蓝色入口不能继续宣称已验证。
- 完整审计失败：查看逐项报告；训练超时、缺凭据和代码错误应分开处理。
- 短训练失败：说明兼容性可能回归，即使旧完整审计曾经通过也应重新验证。
- CodeQL/Scorecard 失败：单独处理安全配置，不能用功能测试成功替代。

## 状态更新规则

验证工作流完成后，更新 `website/notebook-status.json` 或 `website/validation-status.json`，并保留 Action run 链接和准确的验证范围。修改状态后必须重新运行 Build Chinese learning site，让仓库说明和 Site 展示来自同一份数据。
