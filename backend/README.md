# Backend

后端使用 FastAPI 提供论文分析和论文问答 API。当前版本重点是搭建清晰的本地 Agent 后端骨架：请求校验、结构化 schema、Markdown 解析、文本分块、本地文件落盘、关键词检索问答和测试覆盖。

## 模块边界

- `app/api/`：HTTP 路由、请求模型、响应模型和 HTTP 错误转换。
- `app/schemas/`：Pydantic 数据结构，是 API、服务层和落盘 JSON 的共享合同。
- `app/services/`：业务流程编排，当前核心是 `PaperService`。
- `app/parsers/`：Markdown 章节解析和正文分块。
- `app/retrieval/`：检索能力，当前为关键词检索。
- `app/renderers/`：把结构化结果渲染成 Markdown 阅读笔记。
- `app/llm/`：模型调用边界，当前仍是占位实现。
- `app/storage/`：本地文件系统读写。

## 启动

在项目根目录安装依赖：

```bash
C:\Users\Lenovo\miniconda3\python.exe -m pip install -r backend\requirements.txt
```

启动服务：

```bash
cd backend
C:\Users\Lenovo\miniconda3\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

服务默认运行在：

```text
http://127.0.0.1:8000
```

## API

### 健康检查

```bash
curl http://127.0.0.1:8000/health
```

返回示例：

```json
{"status":"ok","service":"Paper-Reading-Agent"}
```

### 分析论文

```http
POST /api/papers/analyze
```

输入标题、摘要和 Markdown 正文后，后端会：

1. 校验摘要和正文不能同时为空。
2. 生成唯一 `paper_id`。
3. 创建 `data/papers/<paper_id>/` 和 `data/outputs/<paper_id>/`。
4. 保存原始 Markdown 为 `paper.md`。
5. 解析章节结构。
6. 生成文本 chunks。
7. 调用占位 `LLMClient` 生成 summary、glossary 和 learning_plan。
8. 保存 `analysis.json`、`chunks.json` 和 `reading_note.md`。

### 论文问答

```http
POST /api/papers/{paper_id}/ask
```

当前问答流程：

1. 根据 `paper_id` 读取 `data/outputs/<paper_id>/chunks.json`。
2. 使用 `KeywordRetriever` 计算问题关键词与 chunk 文本的命中分数。
3. 返回模板化答案和引用片段。

如果找不到 chunks，会返回 404。

## 测试

测试配置位于 `pytest.ini`：

```ini
[pytest]
testpaths = tests
pythonpath = .
addopts = --basetemp=.pytest_tmp_run -p no:cacheprovider
```

运行测试：

```bash
cd backend
C:\Users\Lenovo\miniconda3\python.exe -m pytest
```

也可以从项目根目录运行：

```bash
C:\Users\Lenovo\miniconda3\python.exe -m pytest backend
```

`--basetemp=.pytest_tmp_run` 用于规避 Windows 系统临时目录权限问题；`-p no:cacheprovider` 用于关闭 pytest 缓存写入。

## 后续扩展点

- 将 `LLMClient` 替换为真实模型调用。
- 将 `KeywordRetriever` 替换或扩展为向量检索。
- 增加 PDF parser。
- 增加 SQLite 元数据存储。
- 保存问答历史。
