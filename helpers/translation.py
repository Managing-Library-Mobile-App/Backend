from googletrans import Translator
from googletrans.models import Detected

# from argostranslate import package
# package.install_from_path("translate-en_pl-1_9.argosmodel")
# from argostranslate import translate


# w googletrans można zrobić bulk dla list, batche a może i dict by się dało
# threading, async
# deklaracja klasy raz zamiast za każdym razem
# bez detekcji języka
# lokalny model np. mariana/argos
#


def translate_known_to_known(text_to_translate: str, src: str, language: str) -> str:
    return Translator().translate(text_to_translate, src=src, dest=language).text


def translate_any_to_known(text_to_translate: str, language: str) -> str:
    translator_google = Translator()
    detected_language: Detected = translator_google.detect(text_to_translate)
    if detected_language.confidence < 0.6:
        # raise ValueError(
        #     "Can't translate, the probability is too low:"
        #     + str(detected_language.confidence * 100)
        #     + "%"
        #     + text_to_translate
        # )
        return text_to_translate
    if detected_language.lang == language:
        return text_to_translate
    return translator_google.translate(
        text_to_translate, src=detected_language.lang, dest=language
    ).text


def translate_dict_to_known(
    dict_to_translate: dict, language: str, not_translated: set[str] = None
) -> dict:
    for key, value in dict_to_translate.items():
        if key not in not_translated:
            if isinstance(value, dict):
                dict_to_translate[key] = translate_dict_to_known(
                    value, language, not_translated
                )
            elif (
                isinstance(value, list)
                or isinstance(value, tuple)
                or isinstance(value, set)
            ):
                dict_to_translate[key] = translate_list_to_known(
                    dict_to_translate[key], language, not_translated
                )
            elif isinstance(value, str):
                dict_to_translate[key] = translate_any_to_known(
                    dict_to_translate[key], language
                )
    return dict_to_translate


def translate_list_to_known(
    list_to_translate: list, language: str, not_translated: set[str] = None
) -> list:
    for index, value in enumerate(list_to_translate):
        if isinstance(value, dict):
            list_to_translate[index] = translate_dict_to_known(
                value, language, not_translated
            )
        elif (
            isinstance(value, list)
            or isinstance(value, tuple)
            or isinstance(value, set)
        ):
            list_to_translate[index] = translate_list_to_known(
                list_to_translate[index], language, not_translated
            )
        elif isinstance(value, str):
            list_to_translate[index] = translate_any_to_known(
                list_to_translate[index], language
            )
    return list_to_translate


# def get_argos_model(source, target):
#     lang = f"{source} -> {target}"
#     source_lang = [
#         model
#         for model in translate.get_installed_languages()
#         if lang in map(repr, model.translations_from)
#     ]
#     target_lang = [
#         model
#         for model in translate.get_installed_languages()
#         if lang in map(repr, model.translations_to)
#     ]
#
#     return source_lang[0].get_translation(target_lang[0])
#
#
# argos_en_pl = get_argos_model("English", "Polish")
#
#
# def translate_english_to_polish(text_to_translate: str) -> str:
#     translated_text = argos_en_pl.translate(text_to_translate)


# for i in range(0, 10):
#     translate_english_to_polish("beach please")
#     translate_english_to_polish("welcome here bro")
#     translate_english_to_polish("welcome here bro")
