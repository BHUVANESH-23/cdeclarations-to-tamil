import re
from google.transliteration import transliterate_text # type: ignore
from .data.tamil_data import letters, data_type # type: ignore


def replace_words_with_values(string: str, dictionary: dict[str, str]) -> str:
    pattern = re.compile(
        rf"\b({'|'.join(map(re.escape, dictionary.keys()))})\b")
    replaced_string = pattern.sub(lambda x: dictionary[x.group()], string)
    return replaced_string


def user_def_var(text: str) -> str:
    matches = re.findall(r"\bகட்டமைப்பு\s+(\w+)", text)  # Change to Tamil 'கட்டமைப்பு'
    if matches:
        for i in matches:
            text = text.replace(
                f"கட்டமைப்பு {i}", f"கட்டமைப்பு {variable(i)}", 1)
    matches1 = re.findall(r"\bகூட்டு\s+(\w+)", text)  # Change to Tamil 'கூட்டு'
    if matches1:
        for i in matches1:
            text = text.replace(f"கூட்டு {i}", f"கூட்டு {variable(i)}", 1)
    matches2 = re.findall(r"\bஉள்ளமை\s+(\w+)", text)  # Change to Tamil 'உள்ளமை'
    if matches2:
        for i in matches2:
            text = text.replace(f"உள்ளமை {i}", f"உள்ளமை {variable(i)}", 1)
    matches3 = re.findall(r"\bபகுப்பு\s+(\w+)", text)  # Change to Tamil 'பகுப்பு'
    if matches3:
        for i in matches3:
            text = text.replace(f"பகுப்பு {i}", f"பகுப்பு {variable(i)}", 1)
    return text


def typec_eng(text: str) -> str | None:
    pattern = r"\((.*?)\)"
    matches = re.search(pattern, text)
    return matches.group(1).strip() if matches else None


def arg_var(tamil_text: str) -> str:
    if "(" in tamil_text:
        pattern = r"பணிமுறைகள்\s*(?:\([^)]*\))?\s*மறுசுழற்சி"  # Change to Tamil equivalent 'பணிமுறைகள்' 
        matches = re.findall(pattern, tamil_text)
        pattern1 = r"கூட்டு\s*(?:\([^)]*\))?\s*மறுசுழற்சி"  # Change to Tamil equivalent 'கூட்டு'
        matches1 = re.findall(pattern1, tamil_text)
        matches = matches + matches1
        for index, fun in enumerate(matches):
            type_w: str | None = typec_eng(fun)
            if type_w:
                splt: list[str] = type_w.split(",")
                for index1, args in enumerate(splt):
                    word: str = args.strip()
                    if re.match(r"^[a-zA-Z0-9]+$", word):
                        transliterated_word: str = variable(word)
                        splt[index1] = transliterated_word
                if matches[index].startswith("கூட்டு"):
                    tamil_text = tamil_text.replace(
                        matches[index], f"கூட்டு({','.join(splt)})மறுசுழற்சி", 1
                    )
                else:
                    tamil_text = tamil_text.replace(
                        matches[index], f"பணிமுறைகள்({','.join(splt)})மறுசுழற்சி", 1
                    )
    return tamil_text


def replace_last_occurrence(text: str, old_word: str, new_word: str) -> str:
    words: list[str] = text.rsplit(old_word, 1)
    replaced_text: str = new_word.join(words)
    return replaced_text


def variable(text: str) -> str:
    result: str = ""
    if len(text) > 3:
        text = transliterate_text(text, lang_code="ta")  # Change lang_code to Tamil
        for char in text:
            if char in letters:
                result += letters[char]
            else:
                result += char
        return result
    emptstr: str = ""
    for i in text:
        emptstr += letters[i.upper()]  # Assuming you have Tamil equivalents in 'letters'
    return emptstr


def transt1(text: str) -> str:
    text = re.sub(r"\$ 3", "ஆக", text)  # Change to Tamil equivalent
    text = re.sub(r"\$ ", "க்கு ", text)  # Change to Tamil equivalent
    text = re.sub(r"\$  ", "க்கு ", text)  # Change to Tamil equivalent
    text = re.sub(r"க்கு 3", "ஆக", text)  # Change to Tamil equivalent
    text = re.sub(r"க்கு 7", "ஆக", text)  # Change to Tamil equivalent
    text = re.sub(r"க்கு  வரிசை", " என்னும் வரிசை", text)  # Change to Tamil equivalent
    tamil_text: str = replace_words_with_values(text, data_type)
    return tamil_text
