# 中文课程：运行说明与验证范围

更新日期：2026-09-17。

## 在 Site 运行 Notebook

打开导航中的「运行 Notebook」，选择课程，等待 Python 内核就绪，再选择「运行 → 运行所有单元格」。代码在当前浏览器中执行，使用你的设备算力。首次加载 Python 和依赖需要网络。MNIST 已随站点提供；其他本地文件可以拖入左侧文件区。修改后请下载 Notebook 备份，浏览器存储可能被清理。

以下七个入口已在真实 Chromium 浏览器中逐单元执行，通过检查包括绘图输出错误：

| Notebook | 实际验证范围 |
| --- | --- |
| 家族关系推理 FamilyOntology | 完整教程，14 个浏览器代码单元 |
| 动物专家系统 Animals | 完整教程，9 个浏览器代码单元；默认演示，可切换手动问答 |
| 感知器 Perceptron | 完整教程，27 个代码单元 |
| 自建神经网络框架 OwnFramework | 完整教程，28 个代码单元 |
| 遗传算法 Genetic | 完整教程，17 个代码单元；算法设有最大迭代次数 |
| 多分类感知器 PerceptronMultiClass | 8 个准备代码单元；仍需自己完成练习 |
| 自建框架 MNIST MyFW_MNIST | 6 个准备代码单元；仍需自己完成练习 |

[浏览器执行记录](https://github.com/azfiles/AI-For-Beginners/actions/runs/35070286053)。练习中的留白保留教学用途，准备代码通过不代表练习答案已完成。

## 完整 Python 环境

TensorFlow、PyTorch 等课程使用完整 Python 内核。Site 的 JupyterLite 不提供这些原生框架，也未实现从 Site 远程控制本机内核。可以在本机 JupyterLab 中执行，并复用本地数据和模型缓存。

推荐按[本机环境说明](https://github.com/azfiles/AI-For-Beginners/blob/main/runtime/README.zh-CN.md)使用 Docker。配置面向 Linux x86_64 CPU，包含 Python 3.11、TensorFlow 2.17、Keras 3.5、PyTorch 2.2.2。GPU、macOS 和 Windows 尚未实测。

若不用 Docker，在完整仓库根目录执行：

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install torch==2.2.2 torchvision==0.17.2 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r site/requirements-advanced.txt
python -m pip install jupyterlab
python -m ipykernel install --user --name ai4beg --display-name "AI for Beginners"
python -m jupyter lab
```

上面的 Torch 安装命令面向 Linux CPU。保留完整 lessons、examples、data 和 site 目录，以 Notebook 所在目录为工作目录，选择 AI for Beginners 内核。依赖文件记录直接依赖版本，不是完整传递依赖锁文件。

## 模型、数据与外部服务

- MNIST 随仓库和浏览器课程提供。
- NER 和人体分割支持本地数据；未指定本地路径时尝试下载原始 Kaggle 数据集并缓存。下载失败会明确报错，不会用假数据代替。
- PH2 医学分割数据需从[原作者页面](https://www.fc.up.pt/addi/ph2%20database.html)登记获取。下载解压后设置 PH2_DATA_DIR；站点不重新分发该数据集。
- CLIP 默认使用课程自带的两张图片，也可设置 CLIP_IMAGES_DIR 使用自己的图片。
- MSConceptGraph 需要 NEWSAPI_KEY，或通过 NEWS_TITLES_JSON 提供本地标题字符串数组 JSON 文件；概念查询仍需要网络。
- 其他模型和数据可能在首次运行下载。Docker 的持久化缓存卷可复用下载结果；未验证所有课程完全离线可用。

本地路径变量及目录结构见本机环境说明。Colab 只打开单个文件不会自动取得仓库其他数据和辅助模块，需要自行克隆课程并准备环境，尚未验证其预装环境兼容性。

## 实际验证结果

**尚未达到所有 Notebook 完整执行通过的标准。** 完整训练、短训练测试、练习准备代码和浏览器执行分别记录，不合并为「全部通过」。

已完成的专项测试：

- 本机 Docker 环境：镜像构建、TensorFlow/PyTorch/TorchText 导入、Jupyter 启动、携带 token 访问成功和匿名访问被拒绝均通过。[执行记录](https://github.com/azfiles/AI-For-Beginners/actions/runs/35040738983)。这不等于所有课程执行通过。

- 五份完整浏览器教程和两份练习准备代码：见上表。
- GAN 两种 TensorFlow 网络：真实训练更新后权重变化且损失有限；风格迁移 Keras：实际梯度与图像更新通过。[执行记录](https://github.com/azfiles/AI-For-Beginners/actions/runs/34920542596)。这是短训练验证。
- TensorFlow 自编码器：原 Notebook 全部单元执行，四条训练路径使用 128 张真实 MNIST 图片、各 1 个 epoch。[执行记录](https://github.com/azfiles/AI-For-Beginners/actions/runs/34982157923)。未验证原定长训练效果。
- TensorFlow NLP：文本表示全本、Transformer 全本四条训练路径，以及词嵌入、RNN、生成网络的首个训练路径通过，每次限制两个真实数据批次。[执行记录](https://github.com/azfiles/AI-For-Beginners/actions/runs/35040739031)。不代表后续所有模型均已验证。

最新完整审计已经结束并产出逐项发现；长训练超时、兼容修复后的项目和受限资源项不会自动标成完整通过。[完整审计记录](https://github.com/azfiles/AI-For-Beginners/actions/runs/35072071135)。统一的全单元短训练兼容性运行已经通过 18 个项目，[运行记录](https://github.com/azfiles/AI-For-Beginners/actions/runs/35072489957)。[逐项状态与条件](VALIDATION.zh-CN.md)记录每份文件的验证范围。

NER 和人体分割的原始数据完整下载、解压、结构检查与缓存复用已验证：NER 1,048,575 行，人体分割 1,192 对图像和掩码。[下载验证](https://github.com/azfiles/AI-For-Beginners/actions/runs/35040991992)、[Notebook 验证](https://github.com/azfiles/AI-For-Beginners/actions/runs/35042070696)。

当前完整审计使用真实 Jupyter 内核，逐单元执行，记录异常和输出错误；每份 Notebook 单独隔离目录，完整执行限时 900 秒。超时视为未验证。需要账号、受限数据或学习者完成代码的项目不能自动判为通过。

```bash
python tools/validate_learning.py --workers 1 --timeout 900
```

结果保存在 validation/results.json，包含每个文件状态、执行单元数及源代码摘要。GitHub Actions 使用独立环境分组运行并汇总全部结果；即使失败也会保留报告。短训练测试保留真实数据和模型，明确记录缩减的批次、轮数和所有测试改写，不代表原规模训练完成或模型效果已验收。

## 上游同步

本仓库以中文学习站为主要产品，选择性同步 Microsoft 原始仓库的课程更新，保留课程来源和简体中文翻译；不会为保持上游工程风格而覆盖本站运行环境、验证状态或兼容性修复。
