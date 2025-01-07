import re
from . import translate
from . import preprocess
from .data.tamil_data import data_type  # Change the import to refer to Tamil data

keywords: tuple = (
    "break",
    "case",
    "continue",
    "default",
    "do",
    "else",
    "for",
    "goto",
    "if",
    "return",
    "sizeof",
    "switch",
    "typedef",
    "while",
)


def preprocess_text(text: str) -> tuple[str, str]:
    text = preprocess.args_restruct(text)
    text1: str = text
    sen_list: list[str] = text.split()
    var: str = sen_list[0]
    if sen_list[-1] == "declare":
        text = preprocess.declare_restruct(text)
        if re.search(r"pointer to member of class", text):
            text = preprocess.class_restructd(text1)
    if sen_list[-1] == "cast":
        text = preprocess.cast_restruct(text)
        var = preprocess.cast_var(text)
        if re.search(r"pointer to member of class", text):
            text = preprocess.class_restructc(text)
    return text, var


def translate_text(text: str, var: str) -> str:
    tamil_text: str = translate.replace_words_with_values(text, data_type)  # Use Tamil translation data
    tamil_text = translate.arg_var(tamil_text)
    if tamil_text.endswith(data_type["cast"]):
        tamil_text = translate.replace_last_occurrence(
            tamil_text, var, translate.variable(var))
    else:
        tamil_text = tamil_text.replace(var, translate.variable(var), 1)
    tamil_text = translate.user_def_var(tamil_text)
    tamil_text = translate.transt1(tamil_text)
    return tamil_text


def to_Tamil(text: str) -> str:
    if text == "syntax error":
        return data_type[text]
    if "bad character" in text:
        return (
            translate.replace_words_with_values(text, data_type)
        )

    text, var = preprocess_text(text)
    if var in keywords:
        return data_type["syntax error"]
    tamil_text: str = translate_text(text, var)

    return tamil_text
