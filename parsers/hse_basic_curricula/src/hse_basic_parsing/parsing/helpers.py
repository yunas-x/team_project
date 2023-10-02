import re


def get_speciality_code_matching(text):
    return re.search(r"\b(?:\d{2}.){2}\d{2}\b", text)


def get_speciality_code_list(text):
    return re.findall(r"\b(?:\d{2}.){2}\d{2}\b", text)


def get_words_in_quotes(text):
    return re.search(r"\"(?:[\da-zА-я\-]+[^\S\f\t\r\n]?)+\"", text)
