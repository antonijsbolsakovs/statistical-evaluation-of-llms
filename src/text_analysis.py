import nltk.corpus
import string
import os


nltk.download('words')
english_vocab = set(w.lower() for w in nltk.corpus.words.words())

with open("danish_words.txt", "r", encoding="utf-8") as f:
    danish_text = f.read()

danish_vocab = set(word.lower() for word in danish_text.splitlines() if word)

folder_path = "output"

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = ""
                next(f)
                for line in f:
                    text += line
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                text = ""
                next(f)
                for line in f:
                    text += line

        tokens = [word.strip(string.punctuation).lower() for word in text.split() if word.isalpha()]
        english_only = [w for w in tokens if w in english_vocab and w not in danish_vocab]
        ambiguous_words = [w for w in tokens if w in english_vocab and w in danish_vocab]
        neither = [w for w in tokens if w not in english_vocab and w not in danish_vocab]

        if english_only or ambiguous_words:
            print(f"\nFile: {filename}")
            if english_only:
                print("  English-only words found:", set(english_only))
            if ambiguous_words:
                print("  Possible false friends:", set(ambiguous_words))
            if neither:
                print("neither", set(neither))
