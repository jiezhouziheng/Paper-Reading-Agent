import os

from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
# load_dotenv() 的作用是读取项目根目录的 .env，把里面的配置加载到环境变量里
from app.schemas.paper import GlossaryItem, LearningTask, Summary

# LLM 输出不能直接污染系统，必须先被 Pydantic 校验。要满足 schema
class LLMAnalysisResult(BaseModel):
    summary: Summary
    learning_plan: list[LearningTask]
    glossary: list[GlossaryItem]


class LLMClient:
    """Minimal model-call boundary.

    Replace these placeholder methods with OpenAI or another compatible LLM API.
    """

    # Key 的有效性判断
    def _is_configured_api_key(self, api_key: str) -> bool:
        if not api_key:
            return False
        if api_key in {"your-api-key", "你的_API_Key", "你的 API Key"}:
            return False
        try:
            api_key.encode("ascii")
        except UnicodeEncodeError:
            return False
        return True


    def __init__(self) -> None:
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.model = os.getenv("OPENAI_MODEL", "gpt-5.2").strip()
        self.base_url = os.getenv("OPENAI_BASE_URL", "").strip() or None

        # 保证不管有没有有效 Key，LLMClient 都一定有 self.client 这个属性
        self.client = None
        # 有 OPENAI_API_KEY -> 创建 OpenAI SDK client，没有就还是返回占位实现
        if self._is_configured_api_key(self.api_key):
            client_kwargs = {"api_key": self.api_key}
            if self.base_url:
                client_kwargs["base_url"] = self.base_url
            self.client = OpenAI(**client_kwargs)


    # 做字符截断，初级实现
    def _trim_text(self, text: str, max_chars: int = 12000) -> str:
        text = (text or "").strip()
        if len(text) <= max_chars:
             return text
        return text[:max_chars] + "\n\n[正文过长，已截断。]"


    # Prompt 构造
    def _build_analysis_prompt(
            self,
            title: str,
            abstract: str,
            markdown_body: str = "",
    ) -> str:
        body = self._trim_text(markdown_body)

        return f"""
你是一个科研论文阅读助手。请基于用户提供的论文标题、摘要和正文，生成中文结构化分析。

要求：
1. 只基于输入内容分析，不要编造论文中没有的信息。
2. 如果信息不足，请明确写“原文信息不足”。
3. summary 需要覆盖研究问题、方法、贡献、局限。
4. learning_plan 给出 3 到 5 个学习任务，任务要具体、可执行。
5. glossary 提取 3 到 8 个关键术语，并用适合本科生理解的语言解释。
6. 输出必须符合系统要求的结构，不要输出额外说明。

论文标题：
{title or "未命名论文"}

论文摘要：
{abstract or "无摘要"}

论文正文 Markdown：
{body or "无正文"}
""".strip()


    # 没接入 LLM 时返回占位格式回答
    def _placeholder_analysis(self) -> dict:
        return {
            "summary": {
                "research_problem": "待接入模型后生成研究问题总结。",
                "method": "待接入模型后生成方法总结。",
                "contribution": "待接入模型后生成核心贡献。",
                "limitation": "待接入模型后生成局限性分析。",
            },
            "learning_plan": [
                {
                    "stage": "基础理解",
                    "task": "阅读标题、摘要和引言，确认论文要解决的问题。",
                },
                {
                    "stage": "方法拆解",
                    "task": "梳理论文方法模块，标记不熟悉的术语和公式。",
                },
                {
                    "stage": "后续学习",
                    "task": "根据术语表补充前置知识，并查找相关论文。",
                },
            ],
            "glossary": [
                {
                    "term": "Transformer",
                    "explanation": "一种基于自注意力机制的序列建模架构。",
                },
                {
                    "term": "Attention",
                    "explanation": "让模型把计算重点放到更重要的信息上。",
                },
                {
                    "term": "Embedding",
                    "explanation": "把离散符号映射到连续向量空间。",
                },
            ],
        }


    # 真实 LLM 生成函数
    def _generate_analysis_with_llm(
        self,
        title: str,
        abstract: str,
        markdown_body: str = "",
    ) -> dict:
        if self.client is None:
            return self._placeholder_analysis()

        prompt = self._build_analysis_prompt(
            title=title,
            abstract=abstract,
            markdown_body=markdown_body,
        )

        try:
            response = self.client.responses.parse(
                model=self.model,
                instructions=(
                    "你是一个严谨的科研论文阅读助手。"
                    "你必须只基于用户提供的论文内容生成分析。"
                    "输出必须符合给定结构。"
                ),
                input=prompt,
                text_format=LLMAnalysisResult,
            )
        except Exception as error:
            print(f"LLM analysis failed, fallback to placeholder: {error}")
            return self._placeholder_analysis()

        parsed = response.output_parsed
        return parsed.model_dump(mode="json")


    # 调用 LLM 生成，并把之前的三个冗余函数集成
    def analyze_paper(
        self,
        title: str,
        abstract: str,
        markdown_body: str = "",
    ) -> dict:
        return self._generate_analysis_with_llm(
            title=title,
            abstract=abstract,
            markdown_body=markdown_body,
        )


    def summarize_paper(self, title: str, abstract: str) -> dict[str, str]:
        return self._placeholder_analysis()["summary"]


    def create_learning_plan(self, title: str, abstract: str) -> list[dict[str, str]]:
        return self._placeholder_analysis()["learning_plan"]


    def extract_glossary(self, title: str, abstract: str) -> list[dict[str, str]]:
        return self._placeholder_analysis()["glossary"]
