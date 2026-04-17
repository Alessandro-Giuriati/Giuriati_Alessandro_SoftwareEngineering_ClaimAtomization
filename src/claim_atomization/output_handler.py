from pathlib import Path
import re


def format_claims_as_text(claims: list[str]) -> str:
    """
    Format extracted claims as a readable text block.

    Args:
        claims: List of extracted atomic claims.

    Returns:
        A formatted string ready to be saved to a text file.

    Raises:
        ValueError: If the claims list is empty.
    """
    if not claims:
        raise ValueError("No claims available to format.")

    lines = ["Extracted claims:", ""]

    for index, claim in enumerate(claims, start=1):
        lines.append(f"{index}. {claim}")

    lines.append("")
    lines.append(f"Total claims extracted: {len(claims)}")

    return "\n".join(lines)


def build_output_path(
    article_path: str,
    output_dir: str = "data/output",
) -> str:
    """
    Build a safe output path for the extracted claims file.

    Args:
        article_path: Path of the input article file.
        output_dir: Directory where the output file will be saved.

    Returns:
        A string representing the output file path.
    """
    article_name = Path(article_path).stem
    safe_name = re.sub(r"[^\w]+", "_", article_name).strip("_").lower()

    if not safe_name:
        raise ValueError(
            "Could not derive a valid output filename from the article path."
        )

    output_filename = f"{safe_name}_claims.txt"
    return str(Path(output_dir) / output_filename)


def save_claims_to_txt(claims: list[str], output_path: str) -> None:
    """
    Save extracted claims to a text file.

    Args:
        claims: List of extracted atomic claims.
        output_path: Path of the output text file.

    Raises:
        ValueError: If the output path is empty.
    """
    if not output_path.strip():
        raise ValueError("Output path cannot be empty.")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    formatted_claims = format_claims_as_text(claims)
    path.write_text(formatted_claims + "\n", encoding="utf-8")