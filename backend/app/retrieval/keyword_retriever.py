import re

from app.schemas.paper import AnswerCitation, TextChunk


class KeywordRetriever:
    def retrieve(
        self,
        question: str,
        chunks: list[TextChunk],
        limit: int = 3,
    ) -> list[AnswerCitation]:
        keywords = {
            token.lower()
            for token in re.findall(r"[A-Za-z0-9\u4e00-\u9fff]+", question)
            if token.strip()
        }

        scored: list[tuple[int, TextChunk]] = []

        for chunk in chunks:
            text = chunk.text.lower()
            score = sum(1 for keyword in keywords if keyword in text)

            if score > 0:
                scored.append((score, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)

        return [
            AnswerCitation(
                chunk_id=chunk.chunk_id,
                section_title=chunk.section_title,
                text=chunk.text,
                score=score,
            )
            for score, chunk in scored[:limit]
        ]