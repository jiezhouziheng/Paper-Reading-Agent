# Backend

最小后端模块。

当前使用 FastAPI 提供 API 入口，并按最小职责拆分为：

- `app/api/`：HTTP 路由。
- `app/services/`：业务流程编排。
- `app/llm/`：模型调用封装。
- `app/storage/`：本地数据存储。

## 启动

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

服务默认运行在 `http://localhost:8000`。

## 健康检查

```bash
curl http://localhost:8000/health
```

返回示例：

```json
{"status":"ok","service":"Paper-Reading-Agent"}
```
