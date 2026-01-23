from ai4bharat.transliteration import XlitEngine

_engine = XlitEngine(
    src_script_type="indic",
    beam_width=10,
    rescore=False
)

def transliterate_text(text: str, lang_code: str = "hi") -> str:
    if not text:
        return text

    result = _engine.translit_sentence(
        text,
        lang_code=lang_code
       # topk=1,
       # beam_width=10
    )

    return result

def transliterate_payload(payload: dict, fields: list, normalize: bool):
    result = payload.copy()

    for field in fields:
        if field in result and isinstance(result[field], str):
            result[field] = transliterate_text(result[field])

    return result

