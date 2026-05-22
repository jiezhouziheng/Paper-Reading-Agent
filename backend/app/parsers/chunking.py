from app.schemas.paper import MarkdownSection, TextChunk


def build_text_chunks(
    markdown_body: str,
    sections: list[MarkdownSection],
    max_chars: int = 800,
) -> list[TextChunk]:
    text = markdown_body.strip()

    if not text:
        return []


    chunks: list[TextChunk] = []
    paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]

    current_text = ""
    current_section = sections[0] if sections else MarkdownSection(
        order=1,
        title="正文",
        level=0,
        char_count=len(text),
    )

    for paragraph in paragraphs:
        if len(current_text) + len(paragraph) + 2 > max_chars and current_text:
            chunks.append(
                TextChunk(
                    chunk_id=f"chunk-{len(chunks) + 1:04d}",
                    section_title=current_section.title,
                    section_level=current_section.level,
                    order=len(chunks) + 1,
                    text=current_text.strip(),
                    char_count=len(current_text.strip()),
                )
            )
            current_text = paragraph
        else:
            current_text = f"{current_text}\n\n{paragraph}".strip()

    if current_text:
        chunks.append(
            TextChunk(
                chunk_id=f"chunk-{len(chunks) + 1:04d}",
                section_title=current_section.title,
                section_level=current_section.level,
                order=len(chunks) + 1,
                text=current_text.strip(),
                char_count=len(current_text.strip()),
            )
        )

    return chunks