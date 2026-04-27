from difflib import SequenceMatcher
from pathlib import Path
import re


def build_manual_claims_path(
    article_path: str,
    manual_claims_dir: str = "data/manual_claims",
) -> str:
    """
    Build the expected manual claims file path for a given article.

    Example:
    data/articles/example_article.txt
    -> data/manual_claims/example_article_manual_claims.txt
    """
    article = Path(article_path)
    manual_filename = f"{article.stem}_manual_claims.txt"
    return str(Path(manual_claims_dir) / manual_filename)


def load_manual_claims(manual_claims_path: str) -> list[str]:
    """
    Load manual gold-standard claims from a text file.

    The file may contain plain lines, numbered claims, or bullet points.
    Empty lines are ignored.
    """
    path = Path(manual_claims_path)

    if not path.exists():
        raise FileNotFoundError(f"Manual claims file not found: {manual_claims_path}")

    if not path.is_file():
        raise ValueError(f"Expected a manual claims file, but got: {manual_claims_path}")

    raw_text = path.read_text(encoding="utf-8").strip()

    if not raw_text:
        raise ValueError(f"The manual claims file is empty: {manual_claims_path}")

    claims = []

    for line in raw_text.splitlines():
        cleaned_line = line.strip()

        if not cleaned_line:
            continue

        cleaned_line = re.sub(r"^\s*\d+[\).\-\s]+", "", cleaned_line)
        cleaned_line = re.sub(r"^\s*[-*•]\s+", "", cleaned_line)
        cleaned_line = cleaned_line.strip()

        if cleaned_line:
            claims.append(cleaned_line)

    if not claims:
        raise ValueError(f"No valid manual claims found in: {manual_claims_path}")

    return claims


def normalize_claim(claim: str) -> str:
    """
    Normalize a claim for textual comparison.
    """
    normalized = claim.lower()
    normalized = re.sub(r"[^\w\s]", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def similarity_score(claim_a: str, claim_b: str) -> float:
    """
    Compute a fuzzy similarity score between two claims.
    """
    normalized_a = normalize_claim(claim_a)
    normalized_b = normalize_claim(claim_b)
    return SequenceMatcher(None, normalized_a, normalized_b).ratio()


def evaluate_claims(
    model_claims: list[str],
    manual_claims: list[str],
    match_threshold: float = 0.75,
) -> dict:
    """
    Compare model-generated claims against manual gold-standard claims.

    Returns a dictionary containing:
    - total model claims
    - total manual claims
    - matched claims
    - precision
    - coverage
    - extra model claims
    - missing manual claims
    """
    matched_pairs = []
    used_manual_indexes = set()

    for model_claim in model_claims:
        best_match_index = None
        best_score = 0.0

        for index, manual_claim in enumerate(manual_claims):
            if index in used_manual_indexes:
                continue

            score = similarity_score(model_claim, manual_claim)

            if score > best_score:
                best_score = score
                best_match_index = index

        if best_match_index is not None and best_score >= match_threshold:
            matched_pairs.append(
                {
                    "model_claim": model_claim,
                    "manual_claim": manual_claims[best_match_index],
                    "score": best_score,
                }
            )
            used_manual_indexes.add(best_match_index)

    matched_model_claims = {pair["model_claim"] for pair in matched_pairs}
    matched_manual_indexes = used_manual_indexes

    extra_model_claims = [
        claim for claim in model_claims if claim not in matched_model_claims
    ]

    missing_manual_claims = [
        claim
        for index, claim in enumerate(manual_claims)
        if index not in matched_manual_indexes
    ]

    total_model_claims = len(model_claims)
    total_manual_claims = len(manual_claims)
    total_matched_claims = len(matched_pairs)

    precision = (
        total_matched_claims / total_model_claims
        if total_model_claims > 0
        else 0.0
    )

    coverage = (
        total_matched_claims / total_manual_claims
        if total_manual_claims > 0
        else 0.0
    )

    return {
        "total_model_claims": total_model_claims,
        "total_manual_claims": total_manual_claims,
        "total_matched_claims": total_matched_claims,
        "precision": precision,
        "coverage": coverage,
        "extra_model_claims": extra_model_claims,
        "missing_manual_claims": missing_manual_claims,
        "matched_pairs": matched_pairs,
    }


def format_evaluation_summary(evaluation: dict) -> str:
    """
    Format the evaluation result for terminal output.
    """
    lines = [
        "Manual quality evaluation:",
        f"- Manual claims: {evaluation['total_manual_claims']}",
        f"- Model claims: {evaluation['total_model_claims']}",
        f"- Matched claims: {evaluation['total_matched_claims']}",
        f"- Precision: {evaluation['precision']:.2f}",
        f"- Coverage: {evaluation['coverage']:.2f}",
        f"- Extra model claims: {len(evaluation['extra_model_claims'])}",
        f"- Missing manual claims: {len(evaluation['missing_manual_claims'])}",
    ]

    if evaluation["missing_manual_claims"]:
        lines.append("")
        lines.append("Missing manual claims:")
        for claim in evaluation["missing_manual_claims"]:
            lines.append(f"- {claim}")

    if evaluation["extra_model_claims"]:
        lines.append("")
        lines.append("Extra model claims:")
        for claim in evaluation["extra_model_claims"]:
            lines.append(f"- {claim}")

    return "\n".join(lines)