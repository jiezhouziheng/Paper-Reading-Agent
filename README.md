# Paper-Reading-Agent

Paper-Reading-Agent 是一个面向科研论文阅读的本地 AI Agent 原型项目。当前版本先完成最小可运行闭环：用户输入论文标题、摘要和 Markdown 正文，系统生成结构化阅读结果，并把分析产物保存到本地目录，方便后续继续扩展论文问答、PDF 解析、向量检索和真实大模型调用。

## 当前版本定位

这是项目的初步可运行版本，重点不是一次性完成完整论文智能体，而是先把主流程跑通并把模块边界搭稳：

```text
前端输入
  -> FastAPI 接口接收请求
  -> 服务层生成 paper_id 并编排分析流程
  -> LLMClient 返回占位分析结果
  -> FileStore 创建论文工作区并保存文件
  -> 前端展示结构化阅读报告
```

当前 `LLMClient` 仍是占位实现，还没有接入真实 OpenAI API 或其他大模型服务。

## 已实现功能

- 支持输入论文标题、摘要和 Markdown 正文。
- 后端自动生成唯一 `paper_id`，用于标识单篇论文。
- 根据 `paper_id` 创建本地工作区：
  - `data/papers/<paper_id>/`
  - `data/outputs/<paper_id>/`
- 返回结构化论文分析结果：
  - 论文总结
  - 术语表
  - 学习计划
  - 问答记录占位
  - 生成文件路径
- 自动保存分析产物：
  - `analysis.json`
  - `reading_note.md`
- 前端展示后端健康状态。
- 前端把 JSON 结果渲染为可读阅读报告。
- 提供 `/health` 健康检查接口，便于本地联调。

## 技术栈

- 后端：Python、FastAPI、Pydantic
- 前端：原生 HTML、CSS、JavaScript
- 存储：本地文件系统
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
│   └── app/
│       ├── main.py
│       ├── api/
│       │   └── routes.py
│       ├── services/
│       │   └── paper_service.py
│       ├── llm/
│       │   └── client.py
│       └── storage/
│           └── file_store.py
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

### 2. 使用 conda base 环境

本项目当前使用 conda 的 `base` 环境运行后端。确认 Python 和 uvicorn 可用：

```bash
C:\Users\Lenovo\miniconda3\python.exe --version
C:\Users\Lenovo\miniconda3\python.exe -m uvicorn --version
```

如依赖缺失，在项目根目录执行：

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

页面顶部会显示后端状态：

- `后端状态：可用`：前端可以访问后端接口。
- `后端状态：不可用`：先检查后端是否已在 `127.0.0.1:8000` 启动。

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
  "paper_id": "attention-is-all-you-need-20260521-153012",
  "title": "Attention Is All You Need",
  "source": {
    "type": "markdown",
    "markdown_body_chars": 32
  },
  "summary": {},
  "learning_plan": [],
  "glossary": [],
  "qa": [],
  "artifacts": {
    "paper_dir": "data/papers/<paper_id>",
    "output_dir": "data/outputs/<paper_id>",
    "analysis_json": "data/outputs/<paper_id>/analysis.json",
    "reading_note": "data/outputs/<paper_id>/reading_note.md"
  }
}
```

## 运行产物

每次分析会在本地生成一个独立目录：

```text
data/outputs/<paper_id>/
├── analysis.json
└── reading_note.md
```

其中：

- `analysis.json` 保存完整结构化分析结果，方便后续程序读取。
- `reading_note.md` 保存面向用户阅读的 Markdown 笔记。

## 模块职责

- `backend/app/api/routes.py`：定义 HTTP 接口和请求模型。
- `backend/app/services/paper_service.py`：编排论文分析主流程。
- `backend/app/llm/client.py`：封装模型生成能力，目前为占位实现。
- `backend/app/storage/file_store.py`：负责本地目录创建和文件保存。
- `frontend/src/main.js`：提交论文输入、检查后端状态、渲染分析结果。
- `frontend/src/styles.css`：维护页面基础样式和后端状态样式。

## 当前限制

- 尚未支持 PDF 文件解析。
- 尚未接入真实大模型 API。
- 尚未实现基于论文正文的检索问答。
- 尚未实现多论文管理和历史记录页面。
- 前端仍是原生静态页面，适合当前 MVP 阶段。

## 后续计划

1. 增加最小测试，覆盖 `paper_id` 生成、文件落盘和 API 返回结构。
2. 接入真实 LLM API，替换 `LLMClient` 的占位实现。
3. 增加 Markdown 正文解析，提取章节、参考文献和关键片段。
4. 增加论文问答接口，先基于本地文本片段检索实现。
5. 增加 PDF 解析能力。
6. 扩展前端为更完整的阅读工作台。


**本版本作为初步 MVP 提交**：

```bash
git add README.md backend frontend
git commit -m "feat: build initial paper reading MVP"
```
