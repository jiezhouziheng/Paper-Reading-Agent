# 项目目录结构

当前版本采用“本地文件系统 + FastAPI + 原生前端”的轻量结构。设计目标是先把论文阅读 Agent 的核心链路拆清楚：API 只处理 HTTP，服务层负责编排，解析、分块、检索、渲染、存储和模型调用分别独立。

```text
Paper-Reading-Agent/
├── README.md
├── .gitignore
├── docs/
│   ├── requirements.md
│   └── project_structure.md
├── frontend/
│   ├── README.md
│   ├── index.html
│   └── src/
│       ├── main.js
│       └── styles.css
├── backend/
│   ├── README.md
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── paper.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── paper_service.py
│   │   ├── parsers/
│   │   │   ├── __init__.py
│   │   │   ├── markdown_parser.py
│   │   │   └── chunking.py
│   │   ├── retrieval/
│   │   │   ├── __init__.py
│   │   │   └── keyword_retriever.py
│   │   ├── renderers/
│   │   │   ├── __init__.py
│   │   │   └── reading_note.py
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   └── client.py
│   │   └── storage/
│   │       ├── __init__.py
│   │       └── file_store.py
│   └── tests/
│       ├── conftest.py
│       ├── test_api.py
│       ├── test_paper_service.py
│       ├── test_markdown_parser.py
│       ├── test_chunking.py
│       ├── test_paper_qa.py
│       ├── test_keyword_retriever.py
│       └── test_reading_note_renderer.py
└── data/
    ├── README.md
    ├── papers/
    │   └── .gitkeep
    ├── outputs/
    │   └── .gitkeep
    └── indexes/
        └── .gitkeep
```

## 模块说明

### frontend

前端模块。当前使用原生 HTML、CSS 和 JavaScript，提供一个轻量论文阅读工作流：

- 检查后端健康状态。
- 提交论文标题、摘要和 Markdown 正文。
- 展示结构化分析结果。
- 保存当前 `paper_id`。
- 基于当前论文发起问答，并展示引用片段。

前端当前不引入构建工具，便于快速验证 API 和产品流程。后续如果交互复杂度上升，再考虑升级为 React 或 Vue。

### backend

后端模块。当前使用 FastAPI 作为 API 服务入口，负责接收请求、调用服务层并返回结构化响应。

### backend/app/api

API 路由层。职责是：

- 定义 HTTP 路由。
- 定义请求模型。
- 声明响应模型。
- 把业务异常转换为 HTTP 状态码，例如把缺失 chunks 转换为 404。

这一层不直接写文件、不解析 Markdown、不做检索。

### backend/app/schemas

结构化数据模型层。当前集中在 `paper.py`，定义：

- `PaperAnalysisResult`
- `SourceInfo`
- `MarkdownSection`
- `TextChunk`
- `Summary`
- `LearningTask`
- `GlossaryItem`
- `PaperQuestionAnswer`
- `AnswerCitation`

这些 schema 是后端服务、API 响应、JSON 落盘和前端消费之间的合同。

### backend/app/services

业务流程层。`PaperService` 当前负责两个主流程：

- `analyze()`：输入归一化、`paper_id` 生成、工作区创建、Markdown 保存、章节解析、正文分块、真实或占位 LLM 分析、阅读笔记渲染和分析结果落盘。
- `ask()`：读取指定论文的 `chunks.json`，调用检索器，返回带引用片段的问答结果。

服务层只编排，不应该包含复杂解析、渲染和检索细节。

### backend/app/parsers

文档解析层。

- `markdown_parser.py`：解析 Markdown 标题，生成章节结构。
- `chunking.py`：把 Markdown 正文按段落和最大字符数切成可检索 chunks。

后续 PDF 解析也应放在这一层，避免污染服务层。

### backend/app/retrieval

检索层。当前只有 `KeywordRetriever`，通过问题关键词与 chunk 文本的包含关系计算简单分数。

这个模块是后续向量检索的替换点。未来可以新增 `VectorRetriever`，保持 `PaperService.ask()` 的整体流程不变。

### backend/app/renderers

输出渲染层。当前 `reading_note.py` 负责把结构化分析结果渲染成稳定 Markdown 阅读笔记。

渲染逻辑独立后，服务层不再拼接大量 Markdown 字符串，也便于后续增加学习计划、术语表和问答历史的独立导出。

### backend/app/llm

模型调用模块。当前 `LLMClient` 已接入 OpenAI Python SDK，并保留没有有效 API Key 或调用失败时的占位回退。

这个模块负责读取 `.env` 配置、校验 API Key、构造 prompt、调用 `responses.parse()`、用 `LLMAnalysisResult` 约束模型输出，并将结果转换成项目内部 schema。后续接入兼容 OpenAI 协议的模型服务或扩展 prompt 时，应优先改这个模块，而不是把模型调用散落到服务层或 API 层。

### backend/app/storage

数据存储模块。`FileStore` 当前负责：

- 运行期目录创建。
- 单篇论文工作区创建。
- JSON 保存和读取。
- 文本保存。

后续如果引入 SQLite、对象存储或向量数据库，应保持这里作为存储边界之一。

### backend/tests

自动化测试目录。当前测试覆盖：

- API 健康检查、论文分析、论文问答。
- 服务层分析流程、落盘和异常校验。
- Markdown 章节解析。
- 文本分块。
- 关键词检索。
- 阅读笔记渲染。
- `conftest.py` 提供 `FakeLLMClient`，确保自动化测试不读取真实 `.env`、不调用真实 LLM、不依赖网络。

`pytest.ini` 中设置了：

- `pythonpath = .`：保证从项目根目录或 backend 目录运行测试时都能导入 `app`。
- `--basetemp=.pytest_tmp_run`：规避 Windows 系统临时目录权限问题。
- `-p no:cacheprovider`：关闭 pytest 缓存，避免 `.pytest_cache` 权限问题。

### data

运行期数据目录：

- `data/papers/`：保存用户输入或导入的论文原文，例如 `paper.md`。
- `data/outputs/`：保存 `analysis.json`、`chunks.json`、`reading_note.md`。
- `data/indexes/`：预留给后续向量索引或检索缓存。

这些目录中的运行期文件默认不提交到 Git，只保留 `.gitkeep` 占位文件。

## 当前设计原则

- 先本地闭环，再接外部服务。
- 先稳定 schema，再接真实 LLM。
- LLM 输出必须先经过 Pydantic 校验，再进入服务层、落盘文件和前端展示。
- 先可追溯关键词检索，再升级语义检索。
- 先把服务编排和具体能力拆开，避免后续功能堆进单个文件。
- 每次新增能力都补对应测试，保证重构时有反馈。
