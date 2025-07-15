import os
from gtts import gTTS
import playsound

def load_dictionary(file_path):
    dictionary = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    english, urdu = line.strip().split(':', 1)
                    dictionary[english.strip().lower()] = urdu.strip()
    except FileNotFoundError:
        print("Error: 'dictionary.txt' file not found.")
        return None
    return dictionary

def speak_text(text, lang):
    try:
        tts = gTTS(text=text, lang=lang)
        filename = "temp.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    except Exception as e:
        print("Error during text-to-speech:", str(e))

def main():
    file_path = "dictionary.txt"
    dictionary = load_dictionary(file_path)
    
    if dictionary is None:
        return

    print("\n📘 English-Urdu Dictionary")
    print("Type 'exit' to quit.\n")

    while True:
        word = input("Enter an English word: ").strip().lower()
        if word == 'exit':
            print("Goodbye!")
            break

        meaning = dictionary.get(word)
        if meaning:
            print(f"Urdu Meaning: {meaning}")
            print("🔊 Speaking English word...")
            speak_text(word, 'en')
            print("🔊 Speaking Urdu meaning...")
            speak_text(meaning, 'ur')
        else:
            print("❌ Word not found in dictionary.")

if __name__ == "__main__":
    main()
