from googletrans import Translator

translator = Translator()

def translate_to_russian(text: str) -> str:
    result = translator.translate(text, dest='ru')
    return result.text
