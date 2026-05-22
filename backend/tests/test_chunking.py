from app.parsers.chunking import build_text_chunks
from app.parsers.markdown_parser import parse_markdown_sections


def test_build_text_chunks_from_markdown_body():
    markdown = "# Introduction\nFirst paragraph.\n\nSecond paragraph."
    sections = parse_markdown_sections(markdown)

    chunks = build_text_chunks(markdown, sections, max_chars=100)

    assert len(chunks) == 1
    assert chunks[0].chunk_id == "chunk-0001"
    assert chunks[0].section_title == "Introduction"
    assert "First paragraph." in chunks[0].text


def test_build_text_chunks_splits_long_text():
    markdown = "A" * 20 + "\n\n" + "B" * 20 + "\n\n" + "C" * 20

    chunks = build_text_chunks(markdown, [], max_chars=30)

    assert len(chunks) == 3
    assert chunks[0].order == 1
    assert chunks[1].order == 2
    assert chunks[2].order == 3