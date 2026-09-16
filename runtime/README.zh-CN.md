# 本机 Notebook 环境

浏览器兼容课程可直接在中文版 Site 中运行。PyTorch、TensorFlow 等完整 Python 课程使用此本机环境：代码、模型和数据都留在你的机器上。环境使用 Python 3.11（TensorFlow Text 2.17 提供对应安装包）。当前配置面向 Linux x86_64 CPU；其他架构与 GPU 配置需单独验证。

## 启动

安装 Docker Engine 与 Compose，并完整检出本仓库。在仓库根目录执行：

```bash
cd runtime
mkdir -p local-data
python -c "import secrets; print('JUPYTER_TOKEN=' + secrets.token_urlsafe(32))" > .env
docker compose up --build -d
```

.env 只在首次启动时创建；保留已有文件，不要覆盖或提交凭据。打开 http://127.0.0.1:8888/lab，使用 .env 中的 token 登录，在 lessons 或 examples 中选择 Notebook。服务只暴露在本机回环地址。

Site 中的浏览器运行入口使用 JupyterLite。此本机环境提供独立的完整 JupyterLab 界面，尚未实现从 Site 远程控制本机内核。

## 本地数据

把已有数据放入 runtime/local-data/，容器会在 /local-data/ 只读访问它。在 .env 中按需添加以下变量，然后执行 docker compose up -d 并重启 Notebook 内核：

```dotenv
PH2_DATA_DIR=/local-data/PH2Dataset
NER_DATASET_CSV=/local-data/ner_dataset.csv
BODY_SEGMENTATION_DIR=/local-data/segmentation_full_body_mads_dataset_1192_img
CLIP_IMAGES_DIR=/local-data/cats
NEWS_TITLES_JSON=/local-data/news-titles.json
```

只添加你实际准备好的路径。news-titles.json 的格式是标题字符串数组。若要读取实时新闻，可以设置 NEWSAPI_KEY，替代本地标题文件。

- MNIST 随仓库提供，基础课程不需要重新下载。
- NER 和人体分割课程在未指定本地路径时，尝试从原始 Kaggle 数据集下载并缓存；下载失败会保留明确错误。
- PH2 需按[原作者页面](https://www.fc.up.pt/addi/ph2%20database.html)登记获取并解压，目录应包含 PH2 Dataset images。不将该数据集重新发布到 Site 或 GitHub。
- CLIP 默认使用课程内已有的两张图片，可用自己的图片目录替换。
- 其余课程首次运行可能下载原始模型或数据。缓存命中后可复用，但不代表全部课程已验证完全离线运行。

## 保存与更新

course 数据卷保存 Notebook、修改和课程目录中的数据；model-cache 数据卷保存 Hugging Face、Torch、Keras、TFDS、Gensim 和数据下载缓存。普通容器重建保留这些卷。

镜像升级不会覆盖学习者已修改的文件。更新课程时先下载备份你的 Notebook，再将所需新版课程文件导入 JupyterLab。不要用删除数据卷的方式更新课程。

验证状态以 site/RUNNING.zh-CN.md 和 GitHub Actions 的逐项结果为准。容器能启动、简短训练通过和整本完整执行通过是不同的验证范围。
