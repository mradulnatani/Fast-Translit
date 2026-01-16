from ai4bharat.transliteration import XlitEngine
xlit_engine = XlitEngine(src_script_type="indic", beam_width=10, rescore=False)

def transliterate_text(text: str) -> str:
    retults = xlit_engine.translit_word(text, lang_code="hi", topk=1)
    return results[0] if results else text
