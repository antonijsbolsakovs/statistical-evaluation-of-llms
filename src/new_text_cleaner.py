import os
import re


def clean_text_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    for i, line in enumerate(lines):
        if i < 2:
            cleaned_lines.append(line)
        else:
            cleaned = line.replace('*', '').replace('\n', ' ').replace(',', '').replace('.', '').replace('"', '').replace("'", '').replace("'s", '')
            cleaned_text = re.sub(r'\s+', ' ', cleaned).strip()
            cleaned_lines.append(cleaned_text)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)


if __name__ == "__main__":
    folder_path = "output"

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            output_path = f"extra_cleaned_output/extra_cleaned_{filename}"
            clean_text_file(file_path, output_path)
