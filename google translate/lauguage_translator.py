import googletrans
from googletrans import Translator
import sys

def display_supported_languages():
    languages = googletrans.LANGUAGES
    print("Supported Languages:")
    for key, value in languages.items():
        print(f"{key}: {value}")
    print("\n")

def translate_text(text, src_language, dest_language):
    translator = Translator()
    try:
        translated = translator.translate(text, src=src_language, dest=dest_language)
        return translated.text
    except Exception as e:
        return f"Error: {e}"

def main():
    print("Welcome to the Language Translator CLI")
    display_supported_languages()

    src_language = input("Enter the source language code (e.g., 'en' for English): ").strip().lower()
    dest_language = input("Enter the destination language code (e.g., 'es' for Spanish): ").strip().lower()

    while True:
        text = input("Enter the text to translate (or 'exit' to quit): ")
        if text.lower() == 'exit':
            break
        translation = translate_text(text, src_language, dest_language)
        print(f"Translation: {translation}\n")

if __name__ == "__main__":
    main()
