class LLMClient:
    """Minimal model-call boundary.

    Replace these placeholder methods with OpenAI or another compatible LLM API.
    """

    def summarize_paper(self, title: str, abstract: str) -> dict[str, str]:
        return {
            "research_problem": "待接入模型后生成研究问题总结。",
            "method": "待接入模型后生成方法总结。",
            "contribution": "待接入模型后生成核心贡献。",
            "limitation": "待接入模型后生成局限性分析。",
        }

    def create_learning_plan(self, title: str, abstract: str) -> list[dict[str, str]]:
        return [
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
        ]
