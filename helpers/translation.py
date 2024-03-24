from googletrans import Translator
from googletrans.models import Detected


def translate_any_to_polish(text_to_translate) -> (str, str):
    translator = Translator()
    detected_language: Detected = translator.detect(text_to_translate)
    if detected_language.confidence < 0.6:
        raise ValueError("Can't translate, the probability is too low:" + str(detected_language.confidence * 100) + "%")
    return translator.translate(text_to_translate, src=detected_language.lang, dest='pl').text


def translate_english_to_polish(text_to_translate):
    return Translator().translate(text_to_translate, src='en', dest='pl').text


def translate_any_to_any(text_to_translate, src, dest):
    return Translator().translate(text_to_translate, src=src, dest=dest).text
