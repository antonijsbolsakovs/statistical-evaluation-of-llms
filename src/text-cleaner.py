import os
import re

def smart_replace(text):
    # Erstat * og \n med mellemrum, hvis de sidder mellem to ikke-mellemrumstegn
    text = re.sub(r'(?<=\S)[\*\n](?=\S)', ' ', text)
    # Fjern * og \n hvis de sidder op ad mellemrum (ingen risiko for sammenkædning)
    text = re.sub(r'[\*\n]', '', text)
    return text

# Sti til output-mappen
folder_path = "output"

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)

        # Læs filindhold
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Fjern * og \n med korrekt håndtering
        cleaned = smart_replace(content)

        # Sørg for at Prompt: og Answer: står på egne linjer
        cleaned = re.sub(r'\s*Prompt:', r'\nPrompt:', cleaned)
        cleaned = re.sub(r'\s*Answer:', r'\nAnswer:', cleaned)

        # Fjern dobbelte mellemrum og trim whitespace
        cleaned = re.sub(r' +', ' ', cleaned)
        cleaned = cleaned.strip()

        # Skriv renset tekst tilbage til filen
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(cleaned)

print("Files have been cleaned and saved successfully.")
