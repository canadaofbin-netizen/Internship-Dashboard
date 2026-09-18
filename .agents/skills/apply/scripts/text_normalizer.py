#!/usr/bin/env python3
"""
Text Normalizer for Job Application Forms.

Solves the major PDF parsing and form auto-fill artifacts:
1. Raw PDF bullet glyphs (⚫, ●, ⬤, ▪, ▫, ◆, ⁃, ◦, ‣, etc.) -> converted to standardized clean bullets ('• ')
2. Missing space after bullets ('⚫Engineered', '⬤Automated' -> '• Engineered', '• Automated')
3. Mid-sentence hard line breaks caused by PDF column margins -> unwrapped into smooth, continuous sentences.
4. Trailing hyphen line breaks ('inter-\\nrater' -> 'inter-rater') rejoined seamlessly.
5. Punctuation spacing corrections (missing spaces after commas, semicolons, colons, and periods).
6. Preserves intentional paragraph boundaries (blank lines '\\n\\n') and bullet item separation ('\\n').
"""

import re

# Comprehensive set of Unicode bullet and symbol glyphs encountered in resumes
UNICODE_BULLETS = (
    r"[\u2022\u25cf\u26ab\u2b24\u25cb\u25e6\u2219\u2043\u2023"
    r"\u25aa\u25ab\u25fe\u25fd\u25fc\u25fb\u25a0\u25a1\u25c6\u25c7"
    r"\u2714\u2713\u25ba\u25b6\u00b7]"
)

# Bullet pattern:
# - Unicode bullets: can be followed by 0 or more spaces (e.g. '⚫Engineered', '⬤Automated')
# - ASCII bullets (*, -, +, >, en-dash, em-dash): MUST be followed by 1 or more spaces
# - Plain 'o': MUST be followed by 1 or more spaces so words like 'of', 'on', 'our' are NOT eaten!
BULLET_START_PATTERN = re.compile(rf"^({UNICODE_BULLETS}\s*|[\*\-\+\>–—−]\s+|o\s+)")


def _clean_phrase(text: str) -> str:
    """Cleans up internal spacing and punctuation formatting for a joined item."""
    if not text:
        return ""
    # Normalize non-breaking spaces to standard spaces
    text = text.replace("\u00a0", " ")

    # Protect URLs and emails by replacing them with unique placeholders
    placeholders = []

    def mask_token(match):
        idx = len(placeholders)
        placeholders.append(match.group(0))
        return f"__PROTECTED_TOKEN_{idx}__"

    # Mask URLs first, then email addresses
    masked = re.sub(r'https?://[^\s<>"\']+', mask_token, text)
    masked = re.sub(r"[\w\.\-+]+@[\w\.\-+]+\.[A-Za-z]{2,}", mask_token, masked)

    # Collapse consecutive horizontal whitespace (including tabs and spaces)
    cleaned = re.sub(r"[ \t]+", " ", masked)
    # Add space after comma, semicolon, colon if immediately followed by an alphabetic character
    cleaned = re.sub(r"([,;:])(?=[A-Za-z])", r"\1 ", cleaned)
    # Add space after period if preceded by at least two lowercase letters and immediately followed by an uppercase letter
    # e.g., 'screening.Achieved' -> 'screening. Achieved' (avoids 'Ph.D.', 'U.S.A.', or URLs)
    cleaned = re.sub(r"([a-z]{2,})\.(?=[A-Z])", r"\1. ", cleaned)

    # Restore protected URLs and emails
    for idx, token in enumerate(placeholders):
        cleaned = cleaned.replace(f"__PROTECTED_TOKEN_{idx}__", token)

    return cleaned.strip()


def _join_lines(lines: list[str]) -> str:
    """
    Joins multiple wrapped lines belonging to a single item/paragraph.
    Handles trailing hyphens gracefully (e.g., 'inter-\\n' + 'rater' -> 'inter-rater').
    """
    if not lines:
        return ""

    result = lines[0]
    for nxt in lines[1:]:
        if not nxt:
            continue
        # Check if previous line ended with a hyphen attached to a word (e.g. 'inter-')
        if re.search(r"\w-$", result) and re.match(r"^\w", nxt):
            result = result + nxt
        else:
            result = result + " " + nxt

    return _clean_phrase(result)


def normalize_text(text: str, bullet_char: str = "•") -> str:
    """
    Normalizes text extracted from resumes/PDFs or pasted into application textareas.

    Args:
        text: The raw input string containing potential PDF artifacts.
        bullet_char: The target bullet character to use (default: '•').

    Returns:
        A beautifully formatted, normalized string with clean bullets,
        unwrapped mid-sentence breaks, and proper spacing.
    """
    if not text or not text.strip():
        return ""
    text = text.replace("\u00a0", " ")
    raw_lines = [line.strip() for line in text.splitlines()]

    # Structure: list of paragraphs or list-item blocks
    # Each entry in blocks is a list of (is_bullet: bool, content: str)
    blocks: list[list[tuple[bool, str]]] = []
    current_block: list[tuple[bool, str]] = []

    current_item_lines: list[str] = []
    current_item_is_bullet = False

    def flush_item():
        nonlocal current_item_lines, current_item_is_bullet
        if current_item_lines:
            joined = _join_lines(current_item_lines)
            if joined:
                current_block.append((current_item_is_bullet, joined))
            current_item_lines = []
            current_item_is_bullet = False

    def flush_block():
        nonlocal current_block
        flush_item()
        if current_block:
            blocks.append(current_block)
            current_block = []

    for line in raw_lines:
        if not line:
            # Blank line signifies a paragraph boundary
            flush_block()
            continue

        m = BULLET_START_PATTERN.match(line)
        if m:
            # Line starts a new bullet item
            flush_item()
            content = BULLET_START_PATTERN.sub("", line).strip()
            current_item_is_bullet = True
            if content:
                current_item_lines.append(content)
        else:
            # Continuation line of current item or new paragraph line
            current_item_lines.append(line)

    flush_block()

    rendered_blocks: list[str] = []
    for block in blocks:
        block_lines: list[str] = []
        for is_bullet, content in block:
            if is_bullet:
                block_lines.append(f"{bullet_char} {content}")
            else:
                block_lines.append(content)
        if block_lines:
            rendered_blocks.append("\n".join(block_lines))

    return "\n\n".join(rendered_blocks)


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
        print(normalize_text(input_text))
    else:
        print("Usage: python text_normalizer.py '<text to normalize>'")
