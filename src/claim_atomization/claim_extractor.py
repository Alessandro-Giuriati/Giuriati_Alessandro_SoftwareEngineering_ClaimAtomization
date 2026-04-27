import os
import re

from openai import OpenAI


def extract_claims(article_text: str) -> list[str]:
    """
    Extract atomic factual claims from a preprocessed article using the OpenAI API.

    Args:
        article_text: Preprocessed article text.

    Returns:
        A list of atomic claims in their original order.

    Raises:
        ValueError: If the article text is empty or if no valid claims are returned.
        RuntimeError: If the API key is missing or the API request fails.
    """
    if not article_text.strip():
        raise ValueError("Article text is empty. Cannot extract claims.")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OpenAI API key not found. Please set the OPENAI_API_KEY "
            "environment variable."
        )

    client = OpenAI(api_key=api_key)

    system_prompt = """
    You are an expert assistant for claim atomization.

    Your task is to convert one article into an ordered list of atomic factual claims.

    Goal:
    Extract the minimum set of non-redundant atomic claims needed to preserve the article's central factual content.
    Granularity must be proportional to the article's informational depth, not artificially inflated.

    Definition of a valid claim:
    - A claim is one self-contained factual proposition.
    - It must be specific enough to stand on its own.
    - It must remain faithful to the source text.
    - If uncertainty, attribution, or speculation is present in the source, preserve it explicitly.

    Core rules:
    1. Preserve the original order of information as much as possible.
    2. Each line must contain exactly one atomic factual claim.
    3. Split only when a sentence truly contains more than one distinct factual proposition.
    4. Do not create separate claims for stylistic emphasis, paraphrases, or near-duplicates.
    5. If the same fact is repeated in different wording, keep it only once.
    6. Prefer the smallest non-redundant set of claims that preserves the article's main factual content.
    7. Do not generalize beyond the source text.
    8. Do not invent facts.
    9. Do not explain, comment, summarize, or evaluate.

    What to exclude:
    - Pure opinions, impressions, praise, criticism, or subjective review language unless explicitly attributed and relevant.
    - Rhetorical language, metaphors, hype, or descriptive flourish.
    - Shopping advice, reader guidance, or promotional suggestions.
    - Minor descriptive details that do not materially affect the article's factual content.
    - Repeated restatements of the same fact.

    What to keep:
    - Concrete events, releases, dates, prices, quantities, configurations, technical facts, availability facts, defects, and other verifiable statements.
    - Explicitly attributed judgments only when they are themselves relevant reported content.
    - Reported statements by named people if they add distinct factual content.
    - Comparisons or contrasts only when they express a concrete fact.

    Special handling:
    - For review-like or opinion-heavy articles, keep only the central factual information and explicitly attributed relevant testimony.
    - Do not convert every sentence of a review into a claim.
    - Do not turn subjective driving impressions, praise, or criticism into standalone claims unless they are clearly reported opinions from a named source and relevant to the article.

    Output rules:
    - Output only the claims.
    - One claim per line.
    - No numbering.
    - No bullets.
    - No headings.

    Before producing the final answer, silently check each claim:
    - Is it factual?
    - Is it atomic?
    - Is it non-redundant?
    - Is it central enough to keep?
    If the answer is no, do not output it.
    """

    user_prompt = f"""
    Extract an ordered list of atomic factual claims from the following article.

    Important:
    - Keep only central, non-redundant factual content.
    - Exclude opinions, stylistic phrasing, promotional or shopping advice, and repeated restatements.
    - For review-like passages, keep only concrete factual statements and clearly relevant attributed testimony.
    - Use the minimum number of claims needed to preserve the article's core factual structure.

    Article:
    \"\"\"
    {article_text}
    \"\"\"
    """

    try:
        response = client.responses.create(
            model="gpt-5.4-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
    except Exception as exc:
        raise RuntimeError(f"OpenAI API request failed: {exc}") from exc

    content = response.output_text

    if not content or not content.strip():
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

    if not claims:
        raise ValueError("The model returned no valid claims after cleaning.")

    return claims
