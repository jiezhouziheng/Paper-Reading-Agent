# 项目目录结构

当前版本先采用最小可运行结构，只保留前端、后端、模型调用和数据存储几个清晰模块，避免过早引入复杂架构。

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
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── paper_service.py
│       ├── llm/
│       │   ├── __init__.py
│       │   └── client.py
│       └── storage/
│           ├── __init__.py
│           └── file_store.py
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

前端模块。当前只放一个最小静态页面，用于后续接入论文上传、阅读笔记展示和问答界面。后续如果需要更完整交互，可以再升级为 React 或 Vue 项目。

### backend

后端模块。当前使用 FastAPI 作为最小 API 服务入口，负责接收前端请求、组织业务流程，并调用服务层。

### backend/app/api

API 路由层。只处理 HTTP 请求和响应，不直接写模型调用或文件存储逻辑。

### backend/app/services

业务流程层。负责编排论文分析、阅读笔记生成、学习计划生成等流程。

### backend/app/llm

模型调用模块。负责封装 OpenAI API 或其他兼容大模型 API。后续替换模型供应商时，优先只改这个模块。

### backend/app/storage

数据存储模块。当前先使用本地文件系统保存论文、输出结果和索引缓存。后续可以扩展 SQLite、向量数据库或对象存储。

### data

运行期数据目录：

- `data/papers/`：保存用户上传或导入的论文文件。
- `data/outputs/`：保存生成的阅读笔记、术语表、学习计划等文件。
- `data/indexes/`：保存向量索引或检索缓存。

这些目录中的运行期文件默认不提交到 Git，只保留 `.gitkeep` 占位文件。
