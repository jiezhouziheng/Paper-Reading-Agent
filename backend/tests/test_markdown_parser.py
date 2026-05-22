from app.parsers.markdown_parser import parse_markdown_sections


def test_parse_markdown_sections_from_headings():
    sections = parse_markdown_sections(
        "# Introduction\nIntro text.\n\n## Method\nMethod text."
    )

    assert len(sections) == 2
    assert sections[0].order == 1
    assert sections[0].title == "Introduction"
    assert sections[0].level == 1
    assert sections[0].char_count > 0
    assert sections[1].title == "Method"
    assert sections[1].level == 2


def test_parse_markdown_without_headings():
    sections = parse_markdown_sections("Plain paper body.")

    assert len(sections) == 1
    assert sections[0].title == "正文"
    assert sections[0].level == 0
    assert sections[0].char_count == len("Plain paper body.")
