import re
from openai import OpenAI


def extract_claims(article_text: str) -> list[str]:
    """
    Extract atomic factual claims from a preprocessed article using the OpenAI API.

    Args:
        article_text: Preprocessed article text.

    Returns:
        A list of atomic claims in their original order.
    """
    client = OpenAI()

    system_prompt = """
You are an expert assistant for claim atomization.

Your task is to convert a news article into an ordered list of atomic factual claims.

Rules:
- Preserve the original order of information as much as possible.
- Each line must contain exactly one atomic factual claim.
- Split complex sentences into smaller factual units when appropriate.
- Express each claim directly as a fact.
- Do not use meta-commentary such as "the article states", "the article says", or similar.
- Keep attribution when it is part of the meaning.
- Keep uncertainty or speculation explicit when present in the source.
- Exclude advice, shopping suggestions, reader guidance, and non-central editorial content.
- Do not generalize beyond the specific product, configuration, actor, date, or event mentioned in the text.
- Do not summarise.
- Do not merge multiple facts into one claim.
- Do not invent facts.
- Do not add explanations or commentary.
- Do not number the claims.
- Output only the claims, one per line.
"""

    user_prompt = f"""
Extract atomic factual claims from the following news article.

Article:
\"\"\"
{article_text}
\"\"\"
"""

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response.output_text

    if not content.strip():
        raise ValueError("The model returned no textual content.")

    raw_lines = content.splitlines()
    claims = []

    for line in raw_lines:
        cleaned_line = line.strip()

        if not cleaned_line:
            continue

        cleaned_line = re.sub(r"^\s*[-*]\s+", "", cleaned_line)
        cleaned_line = re.sub(r"^\s*\d+[\).\-\s]+", "", cleaned_line)

        if cleaned_line:
            claims.append(cleaned_line)

    return claims