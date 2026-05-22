from app.schemas.paper import PaperAnalysisResult


def render_reading_note(analysis: PaperAnalysisResult, abstract: str) -> str:
    sections_text = "\n".join(
        f"- H{section.level} {section.title}（{section.char_count} 字符）"
        for section in analysis.sections
    ) or "无"

    glossary_text = "\n".join(
        f"- **{item.term}**：{item.explanation}"
        for item in analysis.glossary
    ) or "无"

    learning_plan_text = "\n".join(
        f"- **{item.stage}**：{item.task}"
        for item in analysis.learning_plan
    ) or "无"

    return (
        f"# {analysis.title}\n\n"
        f"## 1. 基本信息\n\n"
        f"- 论文 ID：{analysis.paper_id}\n"
        f"- 来源类型：{analysis.source.type}\n"
        f"- Markdown 正文字符数：{analysis.source.markdown_body_chars}\n\n"
        f"## 2. 摘要\n\n"
        f"{abstract or '无摘要'}\n\n"
        f"## 3. 论文总结\n\n"
        f"- 研究问题：{analysis.summary.research_problem}\n"
        f"- 方法：{analysis.summary.method}\n"
        f"- 贡献：{analysis.summary.contribution}\n"
        f"- 局限：{analysis.summary.limitation}\n\n"
        f"## 4. 章节结构\n\n"
        f"{sections_text}\n\n"
        f"## 5. 术语表\n\n"
        f"{glossary_text}\n\n"
        f"## 6. 学习计划\n\n"
        f"{learning_plan_text}\n\n"
        f"## 7. 文件位置\n\n"
        f"- analysis_json：{analysis.artifacts.analysis_json}\n"
        f"- reading_note：{analysis.artifacts.reading_note}\n"
    )