# 参与贡献

感谢你改进 AI 入门中文学习站。本仓库接受中文教材修订、Notebook 兼容性修复、浏览器运行支持、完整 Python 环境和站点体验改进。

## 提交前先确认范围

- 只改文字或翻译：检查相对链接、图片和公式。
- 改浏览器 Notebook：不得依赖 CPython 原生扩展、系统命令或未随站点提供的文件，并在真实浏览器中逐单元执行。
- 改 TensorFlow/PyTorch Notebook：保留真实模型和真实数据路径；如缩短训练，必须记录缩减范围。
- 改验证状态：同时提供对应 Action 运行记录和代码哈希，不得把“短训练通过”写成“完整训练通过”。
- 改站点生成器：生成 `site-dist/` 后检查首页、课程页、Notebook 入口、公式、图片和站内链接。

## 本地检查

```bash
python tools/check_repository_contract.py
python website/build.py
```

需要完整 Python 环境时：

```bash
docker compose -f runtime/compose.yaml up --build
```

Notebook 的专项测试脚本位于 `tools/`，GitHub Actions 的适用范围见 [docs/GITHUB_ACTIONS.zh-CN.md](docs/GITHUB_ACTIONS.zh-CN.md)。不要为了让 CI 变绿而跳过失败单元、替换成假数据或吞掉异常。

## Pull Request 说明

请在 PR 中写明：

1. 修改了哪些课程或运行路径；
2. 实际执行了哪些命令或工作流；
3. 使用的是完整训练、短训练还是仅准备代码；
4. 是否需要外部网络、凭据、模型或受限数据；
5. 对站点上的状态标签是否有影响。

## 上游内容和许可

上游课程同步来自 [microsoft/AI-For-Beginners](https://github.com/microsoft/AI-For-Beginners)，请保留原始作者和许可证信息。本仓库不是 Microsoft 官方项目，也不使用原项目的 CLA 流程。提交即表示你有权按仓库的 [MIT License](LICENSE) 提供这些改动；第三方图片、数据和模型仍应遵守各自条款。
