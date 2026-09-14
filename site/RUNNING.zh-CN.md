# 中文课程：运行说明与验证范围

更新日期：2026-09-14。

## 当前进度

- 已同步 Microsoft 上游 536 个提交，上游版本为 `392d0df1b2647cbee104942390551f1ed9e072c8`。
- 本次提交保存五份已经在此前工作环境执行通过的入门 Notebook 修复。恢复会话后运行环境不可用，本次未重新执行。
- 中文站点此前已完成本地构建，但尚未发布；构建目录仍需从原工作环境恢复。
- **未达到“全部学习代码均能正常运行”的验收标准。** 高级课程、外部服务和练习模板仍有未解决问题。

## 从入门示例开始

在完整仓库根目录执行：

```bash
python examples/01-hello-ai-world.py
python examples/02-simple-neural-network.py
python examples/04-text-sentiment.py
```

三个脚本此前均实际执行通过；情感分析示例输入 `quit` 退出。

## 五份已修复且此前执行通过的 Notebook

| Notebook | 修复内容 |
| --- | --- |
| [感知器](../lessons/3-NeuralNetworks/03-Perceptron/Perceptron.ipynb) | 将仓库内 MNIST 的三元组格式适配为课程使用的命名数据集，保留像素缩放语义 |
| [自建神经网络框架](../lessons/3-NeuralNetworks/04-OwnFramework/OwnFramework.ipynb) | 改用 inline 绘图后端、通过 artist.remove() 清理图元、使用 np.nan |
| [Keras 入门](../lessons/3-NeuralNetworks/05-Frameworks/IntroKeras.ipynb) | 将 compile 的指标参数改为显式 metrics，避免被识别为 loss_weights |
| [TensorFlow 入门](../lessons/3-NeuralNetworks/05-Frameworks/IntroKerasTF.ipynb) | 同上 |
| [PyTorch 入门](../lessons/3-NeuralNetworks/05-Frameworks/IntroPyTorch.ipynb) | Lightning 自动选择 CPU/GPU，移除强制 GPU 要求 |

已清除这些 Notebook 的历史输出，避免把上游旧输出误认为本次执行结果。验证采用独立 Python 进程中的 IPython，按顺序执行代码单元；不是对浏览器、Jupyter 界面或 Colab 的验证，也不代表所有模型效果已验收。

此前还执行通过图像分类入门、FamilyOntology、OpenCV、Genetic Notebook。部分实验文件只是模板，不能将其执行完成视为完成实验。

## 本地运行核心课程

本次验证环境为 Linux x86_64、Python 3.12、NumPy 1.26.4、TensorFlow 2.17 / Keras 3.5、PyTorch 2.2.2 CPU。下列直接依赖版本记录于 requirements-learning.txt；这不是覆盖所有高级课程的完整传递依赖锁文件。

```bash
git clone --filter=blob:none --sparse https://github.com/azfiles/AI-For-Beginners.git
cd AI-For-Beginners
git sparse-checkout set lessons data examples site
python3.12 -m venv .venv
source .venv/bin/activate
# Linux CPU：先装成套的 CPU wheel，避免混用 CPU 与 CUDA 的 TorchVision
python -m pip install torch==2.2.2 torchvision==0.17.2 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r site/requirements-learning.txt
python -m pip install jupyterlab
python -m ipykernel install --user --name ai4beg --display-name "AI for Beginners"
python -m jupyter lab
```

macOS 不使用上述 Linux CPU wheel 安装命令，直接安装 requirements-learning.txt；macOS 与 Windows 尚未实测。Windows 激活命令为 `.venv\\Scripts\\Activate.ps1`。

选择 AI for Beginners 内核。保留完整 lessons 与 data 目录，并以 Notebook 所在目录为工作目录，避免辅助模块和相对数据路径失效。

## Colab 与高级课程

Colab 打开单个 Notebook 时不会同时获取仓库数据和辅助模块，需先克隆仓库并切换到相应课程目录。Colab 预装依赖与本次测试环境不同，未保证兼容。

仍需处理的已发现问题包括：

- MSConceptGraph 需要自己的 NewsAPI key；未提供有效账号凭据，不能端到端验证。
- NER 需要额外的 ner_dataset.csv；人体分割需要对应数据集。
- 多个 lab 保留未完成的练习代码，应由学习者补全，不能标为已完成的示例。
- 强化学习代码与 Gym reset/step 新接口不一致。
- 部分高级 Keras 示例使用旧 API，例如 lr 参数、np.int 等。
- CNN、GAN、迁移学习等完整训练超出本次执行时间预算的项目，均不算通过。
- NLP 的最后一轮复测结果因原工作环境不可用，尚未取回，未作为通过依据。
