import re
import regex


def get_speciality_code_matching(text) -> re.Match | None:
    """Finds first occurrence of an entry like "12.12.12" in the text"""

    return re.search(r"\b(?:\d{2}.){2}\d{2}\b", text)


def get_speciality_code_list(text) -> list[str]:
    """Finds all the occurrences of entries like "12.12.12" in the text"""

    return re.findall(r"\b(?:\d{2}.){2}\d{2}\b", text)


def get_speciality_list(text) -> list[tuple[str, str]]:
    """
    Finds all the occurrences of entries like "12.12.12 Экономика" in the text.
    :return: list of tuples with two values, for instance: [(12.12.12, Экономика), ...].
    """

    return re.findall(r"\b((?:\d{2}.){2}\d{2})\s+([А-я'A-z-,.\"]+(?:\s+[А-яA-z-,.\"]+)*)\b", text)


def get_words_in_quotes(text) -> str | None:
    """
    Finds first occurrence of a word that written in quotation marks.
    For example, for the text "Lorem ipsum "maybe" lorem" Match with "maybe" will be returned.
    """
    
    return find_first_match(r"\"(?:[\dA-zА-я\-\.:,;()'ёЁ\/&]+[^\S\f\t\r\n]?)+\"", text)


def remove_initials_from_text(text) -> str:
    # noinspection SpellCheckingInspection
    """Removes an entry like "С. В. Рощин" from text"""

    return re.sub(r"\b[А-Я]\.\s?[А-Я]\.\s+[А-я-]+\b", "", text)


def find_first_match(pattern, text) -> str | None:
    
    try:
        match = regex.search(pattern, text, timeout=5)
    except Exception as e:
        print(e)
        return None

    if match:
        return match[0]

    return None


