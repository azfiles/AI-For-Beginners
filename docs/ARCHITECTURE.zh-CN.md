# 中文学习站架构

## 内容与发布链路

```mermaid
flowchart TD
  A[课程与中文翻译] --> B[website/build.py]
  C[Notebook 状态 JSON] --> B
  D[JupyterLite 内容] --> B
  B --> E[site-dist 静态站点]
  E --> F[GitHub Actions 构建产物]
  F --> G[ChatGPT Site]
```

`site-dist/` 是生成产物，不是手工维护的源目录。课程页面由中文 Markdown、Notebook 阅读视图、本地图片和 KaTeX 资源组合生成。部署时使用 GitHub Action 的 `chinese-learning-site` 产物同步到既有 Site 项目。

## 两类 Notebook 运行路径

```mermaid
flowchart TD
  A[Notebook 入口] --> B{浏览器兼容?}
  B -->|是| C[JupyterLite / Pyodide]
  B -->|否| D[下载 ipynb]
  D --> E[Docker 或本机 Jupyter]
  E --> F[TensorFlow / PyTorch / 本地数据]
```

浏览器支持是显式白名单：`website/prepare_lite.py` 中的 `SPECS` 决定哪些 Notebook 被复制到 JupyterLite。生成副本会清空旧输出、设置 Pyodide 内核并插入依赖安装单元，不修改课程原文件。

完整 Python 路径由 `runtime/` 提供。Docker 卷复用模型和数据缓存，但不会自动分发受限数据或凭据。

## 状态模型

`website/validation-status.json` 保存完整审计及代码摘要。构建时，如果 Notebook 的代码摘要已经变化，旧的完整通过证据不会继续显示。`website/notebook-status.json` 叠加浏览器验证、明确范围的短训练验证，以及需要凭据或受限数据的条件。

因此，Site 构建、浏览器运行、短训练和完整审计彼此独立：任一成功都不能替代其他层级的证据。

## 上游同步边界

上游 Microsoft 仓库是课程内容来源，不是本仓库的界面或工程规范来源。同步时可以吸收课程、翻译、图片和 Notebook 更新，但应人工处理与以下目录的冲突：

- `website/`：站点生成与浏览器运行；
- `site/`：中文运行及验证说明；
- `runtime/`：固定版本完整环境；
- `tools/`：验证与仓库契约；
- `.github/workflows/`：本仓库的构建、验证和安全策略。
