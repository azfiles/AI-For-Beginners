# 浏览器 Notebook 执行后端

状态：部署配置已准备，尚未在持久服务器构建或启动。现有 Site 是阅读站，尚未接入 Notebook 执行接口。

## 结构

Site 展示中文教程并作为操作界面；Jupyter Server 在一台持久 Linux 服务器上运行 Python 内核，执行 PyTorch/TensorFlow，返回输出和图像。Jupyter 提供会话和内核 API：https://jupyter-server.readthedocs.io/en/latest/developers/rest-api.html 。

本配置是 Linux CPU 版本。GPU 版本需要根据目标机器的显卡和驱动另行配置。当前临时工作区不能作为持久执行后端。

## 本地启动

需要服务器已安装 Docker Engine 和 Compose。在完整检出的仓库执行：

```bash
cd runtime
python -c "import secrets; print('JUPYTER_TOKEN=' + secrets.token_urlsafe(32))" > .env
docker compose up --build -d
```

首次创建 .env 后保留它，不要重复生成覆盖已有凭据，也不要提交到 Git。服务绑定服务器的 127.0.0.1:8888；在这台机器上打开 http://127.0.0.1:8888/lab 并使用 .env 中的 token 登录。

要从 Site 访问，需要目标服务器的 HTTPS 入口或私有连接。当前尚未提供服务器地址，因此没有创建入口，也没有在 Site 展示已连接状态。不要直接将未配置 TLS 的 8888 端口开放到公网。

## 模型和数据保留在哪里

- Docker 的 course 数据卷保存 Notebook、学习者修改以及课程相对目录下下载和解压的数据。
- model-cache 数据卷保存 Hugging Face、Torch、Keras、TensorFlow Datasets、Gensim 等缓存。
- 普通容器重建保留数据卷；不要执行 docker compose down -v，除非明确要删除全部学习文件和缓存。
- 更新镜像不会自动覆盖 course 卷里的学习者文件；升级课程时需要保留个人修改，再同步新版本。

课程所需的模型、压缩包和数据集还没有在目标服务器预下载。确定机器后，应按课程资源清单逐项下载、校验并登记缓存位置，再验证断网或缓存命中情况下的执行。需要账号、许可或 API key 的资源无法仅靠公开下载补齐。

## 已知范围

依赖基于仓库记录的 CPU 验证环境。Jupyter 容器本身尚未完成构建测试；完整课程也未全部通过。查看 site/RUNNING.zh-CN.md 和 GitHub Actions 的逐文件执行结果。缓存资源可以减少下载，不会自动修复代码接口、练习占位符或缺失凭据。
