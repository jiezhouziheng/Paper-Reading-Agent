import re

from app.schemas.paper import MarkdownSection


_HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def parse_markdown_sections(markdown_body: str) -> list[MarkdownSection]:
    text = markdown_body.strip()

    if not text:
        return []

    sections: list[MarkdownSection] = []
    current_title = "正文"
    current_level = 0
    current_lines: list[str] = []
    heading_seen = False

    def flush_current_section() -> None:
        content = "\n".join(current_lines).strip()

        if not content and current_title == "正文" and heading_seen:
            return

        sections.append(
            MarkdownSection(
                order=len(sections) + 1,
                title=current_title,
                level=current_level,
                char_count=len(content),
            )
        )

    for line in text.splitlines():
        heading = _HEADING_PATTERN.match(line)

        if heading:
            if heading_seen or "\n".join(current_lines).strip():
                flush_current_section()

            heading_seen = True
            current_level = len(heading.group(1))
            current_title = heading.group(2).strip()
            current_lines = []
            continue

        current_lines.append(line)

    if heading_seen or "\n".join(current_lines).strip():
        flush_current_section()

    return sections