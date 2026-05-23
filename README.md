# Paper-Reading-Agent

Paper-Reading-Agent 是一个面向科研论文阅读的本地 AI Agent 原型项目。当前版本已经从最初的“标题/摘要输入 -> 占位分析 -> 文件落盘”扩展为一个可测试、可追溯、可继续演进的论文阅读工作流：用户输入论文标题、摘要和 Markdown 正文，系统解析章节、生成文本分块、输出结构化阅读结果，并支持基于论文片段的最小问答。

当前 `LLMClient` 仍是占位实现，尚未接入真实 OpenAI API 或其他大模型服务。现阶段重点是先搭稳数据流、模块边界、测试体系和 RAG 前置结构。

## 当前版本定位

当前版本是本地优先的论文阅读 Agent MVP，目标是把后续接入真实 LLM、PDF 解析、向量检索和多论文管理所需的基础边界先搭好：

```text
前端输入标题、摘要、Markdown 正文
  -> FastAPI 接口校验请求
  -> PaperService 生成 paper_id 并编排分析流程
  -> Markdown parser 提取章节结构
  -> Chunking parser 生成可检索文本片段
  -> LLMClient 返回占位总结、术语表和学习计划
  -> Reading note renderer 生成稳定 Markdown 笔记
  -> FileStore 保存 paper.md、analysis.json、chunks.json、reading_note.md
  -> 前端展示分析结果，并基于当前 paper_id 发起论文问答
  -> KeywordRetriever 从 chunks 中检索引用片段
```

## 已实现功能

- 支持输入论文标题、摘要和 Markdown 正文。
- 使用 Pydantic 对请求和响应进行结构化建模。
- 后端自动生成唯一 `paper_id`，包含标题 slug、时间戳和短 UUID 后缀。
- 支持基础输入校验：摘要和 Markdown 正文不能同时为空。
- 保存原始 Markdown 正文到 `data/papers/<paper_id>/paper.md`。
- 解析 Markdown 标题，生成章节结构 `sections`。
- 对 Markdown 正文进行段落级文本分块，生成 `chunks`。
- 保存分析产物：
  - `data/outputs/<paper_id>/analysis.json`
  - `data/outputs/<paper_id>/chunks.json`
  - `data/outputs/<paper_id>/reading_note.md`
- 使用独立 renderer 生成稳定结构的 Markdown 阅读笔记。
- 提供基于关键词检索的最小论文问答接口。
- 问答结果返回引用片段、章节标题和关键词命中分数。
- 前端支持：
  - 后端健康状态检查。
  - 论文分析提交。
  - 分析结果展示。
  - 基于当前 `paper_id` 的论文问答。
- 提供 pytest 测试体系，覆盖服务层、API、Markdown 解析、文本分块、阅读笔记渲染和关键词检索。

## 技术栈

- 后端：Python、FastAPI、Pydantic
- 前端：原生 HTML、CSS、JavaScript
- 存储：本地文件系统
- 测试：pytest、FastAPI TestClient
- 当前检索：关键词匹配
- 运行环境：推荐使用 conda `base` 环境

## 项目结构

```text
Paper-Reading-Agent/
├── README.md
├── docs/
│   ├── requirements.md
│   └── project_structure.md
├── backend/
│   ├── README.md
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── routes.py
│   │   ├── schemas/
│   │   │   └── paper.py
│   │   ├── services/
│   │   │   └── paper_service.py
│   │   ├── parsers/
│   │   │   ├── markdown_parser.py
│   │   │   └── chunking.py
│   │   ├── retrieval/
│   │   │   └── keyword_retriever.py
│   │   ├── renderers/
│   │   │   └── reading_note.py
│   │   ├── llm/
│   │   │   └── client.py
│   │   └── storage/
│   │       └── file_store.py
│   └── tests/
├── frontend/
│   ├── README.md
│   ├── index.html
│   └── src/
│       ├── main.js
│       └── styles.css
└── data/
    ├── papers/
    ├── outputs/
    └── indexes/
```

## 快速开始

### 1. 进入项目目录

```bash
cd D:\programAndCoding\Paper-Reading-Agent
```

### 2. 安装依赖

```bash
C:\Users\Lenovo\miniconda3\python.exe -m pip install -r backend\requirements.txt
```

### 3. 启动后端

```bash
cd backend
C:\Users\Lenovo\miniconda3\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

后端默认运行在：

```text
http://127.0.0.1:8000
```

### 4. 检查健康状态

```bash
curl http://127.0.0.1:8000/health
```

预期返回：

```json
{
  "status": "ok",
  "service": "Paper-Reading-Agent"
}
```

### 5. 打开前端

直接在浏览器中打开：

```text
frontend/index.html
```

页面顶部会显示后端状态。生成论文分析后，问答区域会绑定当前 `paper_id`，可以继续围绕该论文提问。

## API 说明

### 健康检查

```http
GET /health
```

返回示例：

```json
{
  "status": "ok",
  "service": "Paper-Reading-Agent"
}
```

### 分析论文

```http
POST /api/papers/analyze
```

请求体：

```json
{
  "title": "Attention Is All You Need",
  "abstract": "Transformer paper abstract.",
  "markdown_body": "# Introduction\nTransformer body."
}
```

核心返回字段：

```json
{
  "paper_id": "attention-is-all-you-need-20260523-120000-a1b2c3d4",
  "title": "Attention Is All You Need",
  "source": {
    "type": "markdown",
    "markdown_body_chars": 32,
    "markdown_path": "data/papers/<paper_id>/paper.md"
  },
  "sections": [
    {
      "order": 1,
      "title": "Introduction",
      "level": 1,
      "char_count": 17
    }
  ],
  "chunks": [
    {
      "chunk_id": "chunk-0001",
      "section_title": "Introduction",
      "section_level": 1,
      "order": 1,
      "text": "# Introduction\nTransformer body.",
      "char_count": 32
    }
  ],
  "summary": {},
  "learning_plan": [],
  "glossary": [],
  "qa": [],
  "artifacts": {
    "paper_dir": "data/papers/<paper_id>",
    "output_dir": "data/outputs/<paper_id>",
    "analysis_json": "data/outputs/<paper_id>/analysis.json",
    "reading_note": "data/outputs/<paper_id>/reading_note.md",
    "chunks_json": "data/outputs/<paper_id>/chunks.json"
  }
}
```

### 论文问答

```http
POST /api/papers/{paper_id}/ask
```

请求体：

```json
{
  "question": "How does attention work?"
}
```

返回示例：

```json
{
  "paper_id": "attention-paper-20260523-120000-a1b2c3d4",
  "question": "How does attention work?",
  "answer": "根据当前检索到的论文片段，相关内容主要集中在：Method",
  "citations": [
    {
      "chunk_id": "chunk-0001",
      "section_title": "Method",
      "text": "# Method\nAttention computes weighted token representations.",
      "score": 1
    }
  ]
}
```

当前问答使用关键词检索，`score` 表示问题关键词在片段中的命中数量，不代表模型置信度。

## 运行产物

每次分析会在本地生成独立目录：

```text
data/papers/<paper_id>/
└── paper.md

data/outputs/<paper_id>/
├── analysis.json
├── chunks.json
└── reading_note.md
```

其中：

- `paper.md` 保存用户输入的原始 Markdown 正文。
- `analysis.json` 保存完整结构化分析结果。
- `chunks.json` 保存后续检索和问答使用的文本片段。
- `reading_note.md` 保存面向用户阅读的稳定 Markdown 笔记。

## 模块职责

- `backend/app/api/routes.py`：定义 HTTP 接口、请求模型、响应模型和 HTTP 错误转换。
- `backend/app/schemas/paper.py`：定义论文分析、文本分块、问答引用等共享数据结构。
- `backend/app/services/paper_service.py`：编排论文分析和问答主流程。
- `backend/app/parsers/markdown_parser.py`：解析 Markdown 标题并生成章节结构。
- `backend/app/parsers/chunking.py`：把正文切分成可检索文本片段。
- `backend/app/retrieval/keyword_retriever.py`：基于关键词命中检索相关 chunks。
- `backend/app/renderers/reading_note.py`：生成稳定结构的 Markdown 阅读笔记。
- `backend/app/llm/client.py`：封装模型生成能力，目前为占位实现。
- `backend/app/storage/file_store.py`：负责本地目录创建、JSON 读写和文本保存。
- `frontend/src/main.js`：检查后端状态、提交分析请求、维护当前 `paper_id`、提交问答请求并渲染结果。
- `frontend/src/styles.css`：维护页面基础布局和表单样式。

## 测试

后端测试配置在 `backend/pytest.ini`：

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

测试覆盖：

- API 健康检查、论文分析和论文问答。
- `PaperService` 的分析、落盘和问答流程。
- Markdown 章节解析。
- 正文 chunking。
- 关键词检索。
- 阅读笔记渲染。

## 当前限制

- 尚未支持 PDF 文件解析。
- 尚未接入真实大模型 API，`LLMClient` 仍返回占位结果。
- 问答目前是关键词检索和模板化回答，还不是 LLM 生成答案。
- chunks 的章节归属仍较粗略，当前优先保证可检索片段的数据流。
- 尚未实现多论文列表、历史记录、标签和元数据管理。
- 前端仍是原生静态页面，适合当前 MVP 阶段。

## 后续计划

1. 优化 chunking，使每个 chunk 精确绑定所属章节。
2. 接入真实 LLM API，替换 `LLMClient` 占位实现。
3. 将问答升级为“检索 chunks -> LLM 基于引用片段生成答案”。
4. 增加 PDF 解析能力。
5. 增加论文历史记录和多论文管理。
6. 引入 SQLite 保存论文元数据和问答历史。
7. 引入向量检索，实现语义级 RAG。
