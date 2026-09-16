# Notebook 验证交接记录

更新：2026-09-16。以下范围不可互相替代：浏览器执行、原数据短训练、原始训练规模完整执行。

## 已验证的修复

- [Scorecard](https://github.com/azfiles/AI-For-Beginners/actions/runs/35071580736) 已通过。根因是旧 v3 artifact 上传组件；只改 artifact 名称未能修复。工作流通过不意味着安全评分中的依赖漏洞已全部处理。
- [长 Notebook 全单元短训练](https://github.com/azfiles/AI-For-Beginners/actions/runs/35071580708)：12 项中 11 项通过；TransferLearningTF 在本轮发现解冻后优化器不识别新参数的问题。
- [TransferLearningTF 专项回归](https://github.com/azfiles/AI-For-Beginners/actions/runs/35072071138)：修复后通过。解冻后用新的低学习率 Adam 重新编译，再执行微调。
- CIFAR 两本 Notebook 使用原始 50,000 张训练图、10,000 张测试图，下载包通过 Keras 官方 SHA-256 校验。短测只缩短训练轮数和批次，没有替换数据。
- [资源 Notebook](https://github.com/azfiles/AI-For-Beginners/actions/runs/35070286115)、[本机运行时](https://github.com/azfiles/AI-For-Beginners/actions/runs/35070286191)、[NLP 短测](https://github.com/azfiles/AI-For-Beginners/actions/runs/35070286160)、[浏览器执行](https://github.com/azfiles/AI-For-Beginners/actions/runs/35070286053)、[符号推理](https://github.com/azfiles/AI-For-Beginners/actions/runs/35070286105) 均通过。
- [Embeddings / DeepRL](https://github.com/azfiles/AI-For-Beginners/actions/runs/35070286132) 通过：Embeddings 是真实数据短训练，DeepRL 包含原 100,000 回合与 GIF 输出验证。

## 更正历史结论

`f7393577` 的六项 TensorFlow 短测在引导代码字符串格式化时失败，未执行到课程代码，不应解释为训练超时。该脚本错误已撤回；此前两个使用合成 CIFAR 数据的通过记录不计入原数据验收。

旧审计被新提交取消后，可能没有完整结果文件。报告工作流现在跳过由取消事件触发的聚合；真实失败审计仍保留失败，未采用 continue-on-error 将其变绿。

## 未完成 / 外部条件

- [新的原始规模全量审计](https://github.com/azfiles/AI-For-Beginners/actions/runs/35072071135) 尚需等待终态；短训练结果不能替代它。历史的 35 通过、15 超时、6 失败、1 无代码不是当前源码的新验收结果。
- SemanticSegmentationTF / SemanticSegmentationPytorch 需要合法取得的 PH2 数据，设置 `PH2_DATA_DIR`；尚未完成真实数据训练验证。
- MSConceptGraph 需要 `NEWS_TITLES_JSON` 本地标题数组或 `NEWSAPI_KEY`；概念查询仍依赖外部网络。不要在聊天或仓库中提交密钥。
- 完整 TensorFlow / PyTorch 课程使用本机运行时；Site 的 JupyterLite 不等于能在浏览器执行全部课程。

## CIFAR 缓存预备

在检出仓库的根目录运行 `python tools/prepare_cifar.py`。已有原始压缩包时设置 `CIFAR10_ARCHIVE` 为其路径。脚本只接受与 Keras 官方 SHA-256 一致的包，同时预备 Keras 与 torchvision 的课程缓存。运行需 Python 3.11.8+ 与 curl。

后续状态以对应提交的 Actions 结果为准。长 Notebook 工作流现在也会在课程源码或依赖变更后触发，避免仅修改 Notebook 时没有回归。
