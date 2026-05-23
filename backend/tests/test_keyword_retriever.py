from app.retrieval.keyword_retriever import KeywordRetriever
from app.schemas.paper import TextChunk


def test_keyword_retriever_returns_matching_chunks():
    retriever = KeywordRetriever()
    chunks = [
        TextChunk(
            chunk_id="chunk-0001",
            section_title="Method",
            section_level=1,
            order=1,
            text="Attention computes weighted token representations.",
            char_count=52,
        ),
        TextChunk(
            chunk_id="chunk-0002",
            section_title="Experiment",
            section_level=1,
            order=2,
            text="The model is evaluated on translation datasets.",
            char_count=46,
        ),
    ]

    citations = retriever.retrieve(
        question="How does attention work?",
        chunks=chunks,
    )

    assert len(citations) == 1
    assert citations[0].chunk_id == "chunk-0001"
    assert citations[0].score > 0


def test_keyword_retriever_returns_empty_when_no_match():
    retriever = KeywordRetriever()
    chunks = [
        TextChunk(
            chunk_id="chunk-0001",
            section_title="Method",
            section_level=1,
            order=1,
            text="Attention computes weighted token representations.",
            char_count=52,
        )
    ]

    citations = retriever.retrieve(
        question="dataset benchmark",
        chunks=chunks,
    )

    assert citations == []