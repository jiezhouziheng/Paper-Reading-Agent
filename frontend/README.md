# Frontend

前端当前使用原生 HTML、CSS 和 JavaScript，不依赖构建工具。它的目标是验证论文阅读 Agent 的核心用户流程，而不是先引入复杂前端框架。

## 当前能力

- 检查后端 `/health` 状态。
- 输入论文标题、摘要和 Markdown 正文。
- 调用 `/api/papers/analyze` 生成分析结果。
- 展示论文 ID、总结、术语表、学习计划和文件位置。
- 保存当前 `paper_id`。
- 在分析完成后启用论文问答。
- 调用 `/api/papers/{paper_id}/ask`。
- 展示回答和引用 chunk。

## 本地预览

先启动后端：

```bash
cd backend
C:\Users\Lenovo\miniconda3\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

然后直接在浏览器中打开：

```text
frontend/index.html
```

## 页面状态

- `后端状态：等待检查`：页面刚加载，尚未完成健康检查。
- `后端状态：可用`：前端可以访问后端 API。
- `后端状态：不可用`：后端未启动、端口不对或浏览器无法访问 API。
- `论文问答` 按钮初始禁用，只有成功生成分析并获得 `paper_id` 后才启用。

## 设计说明

当前前端维护一个内存状态：

```js
let currentPaperId = null;
```

分析成功后，`currentPaperId` 会更新为后端返回的 `paper_id`。问答请求依赖这个值来确定问题属于哪篇论文。

这个设计让前端流程保持清晰：

```text
生成分析 -> 获取 paper_id -> 基于 paper_id 提问
```

后续如果引入多论文历史列表，可以把 `currentPaperId` 扩展成“当前选中的论文”状态。

## 后续计划

- 增加论文历史列表。
- 增加引用片段的结构化展示。
- 增加 loading 和错误状态的细分。
- 支持文件上传。
- 当交互复杂度明显上升后，再考虑升级为 React 或 Vue。
