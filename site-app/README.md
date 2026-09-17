# Site 服务端

本目录把 `website/build.py` 生成的 `site-dist/` 与用户级学习记录服务组合为可部署的 ChatGPT Site Worker。

- `worker/index.js`：从平台身份头获取用户 ID，提供 `/api/learning`，其他请求交给静态资源绑定。
- `db/schema.ts` 与 `drizzle/`：D1 表结构和不可变生产迁移。
- `test/`：身份隔离、跨站写入、迁移和静态资源转发测试。
- `scripts/build.mjs`：生成 `site-app-dist/client`、`server` 与迁移。

服务端从不接受客户端提交的用户 ID；所有数据操作都使用 `oai-authenticated-user-id`。
