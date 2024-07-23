import googletrans
from googletrans import Translator, LANGUAGES
import sys

def display_supported_languages():
    print("Supported Languages:")
    for key, value in LANGUAGES.items():
        print(f"{key}: {value}")
    print("\n")

def is_supported_language(lang_code):
    return lang_code in LANGUAGES

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

    src_language = input("Enter the source language code (e.g., 'en' for English, leave blank for auto-detect): ").strip().lower()
    if src_language and not is_supported_language(src_language):
        print(f"Error: Unsupported source language code '{src_language}'. Please try again.")
        return

    dest_language = input("Enter the destination language code (e.g., 'es' for Spanish): ").strip().lower()
    if not is_supported_language(dest_language):
        print(f"Error: Unsupported destination language code '{dest_language}'. Please try again.")
        return

    while True:
        text = input("Enter the text to translate (or 'exit' to quit): ").strip()
        if text.lower() == 'exit':
            break
        if not text:
            print("Error: No text entered. Please enter the text to translate.")
            continue

        translation = translate_text(text, src_language if src_language else 'auto', dest_language)
        print(f"Translation: {translation}\n")

if __name__ == "__main__":
    main()
