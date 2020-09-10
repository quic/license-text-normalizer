# Copyright (c) 2020, Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

"""
Normalizes license text.
"""

from typing import List, Optional


DEFAULT_LEADING_DELIMITERS: List[str] = [
    "@REM #",
    '.\\"',
    "///",
    "//",
    "##",
    "/*",
    "#*",
    ";",
    "**",
    "::",
    ";*",
    "#",
    "*",
    "-",
    "@echo",
]


DEFAULT_BULLET_DELIMITERS: List[str] = ["*", "-"]


DEFAULT_TRAILING_DELIMITERS: List[str] = ["*/", "*;", "*"]

DEFAULT_WORDS_TO_STRIP: List[str] = ["\0", "echo", "dnl", "<BR>", "\\x00"]


def normalize_license_text(
    text: str,
    leading_delimiters: Optional[List[str]] = None,
    bullet_delimiters: Optional[List[str]] = None,
    trailing_delimiters: Optional[List[str]] = None,
    words_to_strip: Optional[List[str]] = None,
) -> str:
    """
    Normalizes the provided text and returns it.
    """
    if not leading_delimiters:
        leading_delimiters = DEFAULT_LEADING_DELIMITERS
    if not bullet_delimiters:
        bullet_delimiters = DEFAULT_BULLET_DELIMITERS
    if not trailing_delimiters:
        trailing_delimiters = DEFAULT_TRAILING_DELIMITERS
    if not words_to_strip:
        words_to_strip = DEFAULT_WORDS_TO_STRIP

    # sort delimiters, longest-to-shortest
    leading_delimiters = sorted(leading_delimiters, key=len, reverse=True)
    bullet_delimiters = sorted(bullet_delimiters, key=len, reverse=True)
    trailing_delimiters = sorted(trailing_delimiters, key=len, reverse=True)
    words_to_strip = sorted(words_to_strip, key=len, reverse=True)
    # create lookup to catch standalone delimiters
    delimiters_lookup = set(leading_delimiters) | set(trailing_delimiters)

    normalized_lines = []
    prev_line = ""
    for raw_line in text.splitlines():
        normalized_line = raw_line.strip()
        # strip standalone delimiter
        if normalized_line in delimiters_lookup:
            normalized_line = ""
        # strip trailing, leading, and bullet delimiters
        normalized_line = _strip_trailing_delimiters(
            normalized_line, trailing_delimiters
        )
        normalized_line = _strip_leading_delimiters(
            normalized_line, leading_delimiters, bullet_delimiters
        )
        # strip lines of all non-alphanumeric characters
        if _is_line_non_alnum(normalized_line):
            normalized_line = ""
        # strip words
        normalized_line = _strip_words(normalized_line, words_to_strip)
        # drop excess (repeated) blank lines
        if normalized_line or prev_line:
            normalized_lines.append(normalized_line)
        prev_line = normalized_line
    return "\n".join(normalized_lines).strip()


def _strip_leading_delimiters(
    line: str, leading_delimiters: List[str], bullet_delimiters: List[str]
) -> str:
    # short-circuit blank lines and lines without leading delimiters
    if not line or line[0].isalnum():
        return line
    # strip leading delimiter
    line = _strip_delimiter(line, leading_delimiters).lstrip()
    # short-circuit if leading special characters depleted
    if not line or line[0].isalnum():
        return line
    # strip bullet delimiter
    return _strip_delimiter(line, bullet_delimiters).lstrip()


def _strip_trailing_delimiters(
    line: str, trailing_delimiters: List[str]
) -> str:
    if not line or line[-1].isalnum():
        return line
    return _strip_delimiter(line, trailing_delimiters, leading=False).rstrip()


def _strip_delimiter(line: str, delimiters: List[str], leading=True) -> str:
    line_starts_or_ends_with = (
        getattr(line, "startswith") if leading else getattr(line, "endswith")
    )
    strip = _strip_leading if leading else _strip_trailing

    for delimiter in delimiters:
        if line == delimiter:
            return ""
        if len(line) < len(delimiter):
            continue
        if line_starts_or_ends_with(delimiter):
            line = strip(line, delimiter)
            break
    return line


def _strip_leading(line: str, delimiter: str) -> str:
    return line[len(delimiter) :]  # noqa


def _strip_trailing(line: str, delimiter: str) -> str:
    return line[: len(delimiter) * -1]


def _strip_words(line: str, words_to_strip: List[str]) -> str:
    normalized_line = line
    for word in words_to_strip:
        normalized_line = "".join(normalized_line.split(word))
    return normalized_line.lstrip()


def _is_line_non_alnum(line: str) -> bool:
    if not len(line) > 1:
        return False
    return not any(char.isalnum() for char in line)
