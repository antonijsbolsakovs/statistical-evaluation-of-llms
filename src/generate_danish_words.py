import csv


with open("ddo_fullforms_2023-10-11.csv", "r") as f:
    reader = csv.reader(f, delimiter="\t")
    danish_words = []
    for row in reader:
        word = row[0]
        danish_words.append(word)
    danish_words = set(danish_words)

with open("danish_words.txt", "a") as file:
    for word in danish_words:
        file.write(word + '\n')
