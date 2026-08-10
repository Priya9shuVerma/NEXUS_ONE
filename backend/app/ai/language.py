import re
from langdetect import detect


def detect_language(text: str) -> str:

    text = text.strip()

    if not text:
        return "English"

    lower = text.lower()

    # Remove punctuation before word-based language detection.
    normalized = re.sub(r"[\W_]+", " ", lower, flags=re.UNICODE).strip()
    words = set(normalized.split())

    # ==========================
    # Roman Bhojpuri
    # ==========================

    bhojpuri_words = {
        "hamaar",
    "hamar",
        "tohar",
        "ketna",
        "ba",
        "batawa",
        "rahal",
        "bhail",
        "kailas",
        "kaisan",
    }

    if words.intersection(bhojpuri_words):
        return "Roman Bhojpuri"

    # ==========================
    # Hinglish / Roman Hindi
    # ==========================

    hinglish_words = {
        "mera",
        "meri",
        "mere",
        "mujhe",
        "mujh",
        "aapka",
        "aapki",
        "apna",
        "apni",
        "kitna",
        "kitni",
        "kya",
        "kaise",
        "kaisa",
        "batao",
        "bata",
        "hai",
        "hain",
        "hua",
        "hui",
        "karna",
        "karo",
        "chahiye",
        "kyon",
        "kyu",
        "kyunki",
    }

    if words.intersection(hinglish_words):
        return "Hinglish"

    # ==========================
    # Spanish
    # ==========================

    spanish_words = {
        "qu?",
        "que",
        "cu?l",
        "cual",
        "cu?les",
        "cuales",
        "c?mo",
        "como",
        "d?nde",
        "donde",
        "cu?ndo",
        "cuando",
        "qui?n",
        "quienes",
        "qui?nes",
        "quien",
        "mi",
        "mis",
        "tu",
        "tus",
        "es",
        "son",
        "tengo",
        "tiene",
        "cu?nto",
        "cu?nta",
        "cu?ntos",
        "cu?ntas",
    }

    if words.intersection(spanish_words):
        return "Spanish"

    # ==========================
    # Marathi
    # MUST BE BEFORE HINDI
    # ==========================

    marathi_words = {
        "????",
        "????",
        "????",
        "??????",
        "???",
        "????",
        "???",
        "????",
        "???",
        "???",
        "????",
        "??????",
        "??????",
        "???????",
        "???????????",
        "?????????",
        "????",
        "????",
        "????",
        "??????",
    }

    if words.intersection(marathi_words):
        return "Marathi"

    # ==========================
    # Sanskrit
    # MUST BE BEFORE HINDI
    # ==========================

    sanskrit_words = {
        "??",
        "????",
        "????",
        "????",
        "?????",
        "?????",
        "?????",
        "?????",
        "????",
        "????",
        "?????",
        "???",
        "??",
        "??",
        "??",
        "?????",
        "??????",
        "???????",
        "????????",
        "?????????",
        "????",
        "??????",
        "??",
    }

    if words.intersection(sanskrit_words):
        return "Sanskrit"

    # ==========================
    # Bengali
    # ==========================

    if any("\u0980" <= char <= "\u09FF" for char in text):
        return "Bengali"

    # ==========================
    # Punjabi / Gurmukhi
    # ==========================

    if any("\u0A00" <= char <= "\u0A7F" for char in text):
        return "Punjabi"

    # ==========================
    # Gujarati
    # ==========================

    if any("\u0A80" <= char <= "\u0AFF" for char in text):
        return "Gujarati"

    # ==========================
    # Tamil
    # ==========================

    if any("\u0B80" <= char <= "\u0BFF" for char in text):
        return "Tamil"

    # ==========================
    # Telugu
    # ==========================

    if any("\u0C00" <= char <= "\u0C7F" for char in text):
        return "Telugu"

    # ==========================
    # Kannada
    # ==========================

    if any("\u0C80" <= char <= "\u0CFF" for char in text):
        return "Kannada"

    # ==========================
    # Malayalam
    # ==========================

    if any("\u0D00" <= char <= "\u0D7F" for char in text):
        return "Malayalam"

    # ==========================
    # Japanese
    # ==========================

    if any(
        ("\u3040" <= char <= "\u30FF")
        or ("\u4E00" <= char <= "\u9FFF")
        for char in text
    ):
        return "Japanese"

    # ==========================
    # Devanagari Hindi
    # ==========================

    if any("\u0900" <= char <= "\u097F" for char in text):

        try:
            lang = detect(text)

            if lang == "sa":
                return "Sanskrit"

            if lang == "mr":
                return "Marathi"

            if lang == "hi":
                return "Hindi"

        except Exception:
            pass

        return "Hindi"

    # ==========================
    # langdetect fallback
    # ==========================

    try:
        lang = detect(text)
    except Exception:
        return "English"

    language_map = {
        "en": "English",
        "hi": "Hindi",
        "ta": "Tamil",
        "te": "Telugu",
        "kn": "Kannada",
        "ml": "Malayalam",
        "bn": "Bengali",
        "mr": "Marathi",
        "gu": "Gujarati",
        "pa": "Punjabi",
        "sa": "Sanskrit",
        "ja": "Japanese",
        "fr": "French",
        "es": "Spanish",
    }

    return language_map.get(lang, "English")
