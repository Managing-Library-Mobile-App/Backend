from googletrans import Translator
from googletrans.models import Detected


def translate_known_to_known(text_to_translate: str, src: str, dest: str) -> str:
    return Translator().translate(text_to_translate, src=src, dest=dest).text


def translate_any_to_known(text_to_translate: str, dest: str) -> str:
    translator = Translator()
    detected_language: Detected = translator.detect(text_to_translate)
    if detected_language.confidence < 0.6:
        raise ValueError("Can't translate, the probability is too low:" + str(detected_language.confidence * 100) + "%")
    if detected_language.lang == dest:
        return text_to_translate
    return translator.translate(text_to_translate, src=detected_language.lang, dest=dest).text


def translate_dict_to_known(dict_to_translate: dict, dest: str, keys: list[str]) -> dict:
    for key in keys:
        dict_to_translate[key] = translate_any_to_known(dict_to_translate[key], dest)
    return dict_to_translate
