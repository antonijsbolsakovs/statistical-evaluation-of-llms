import glob
import os
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from nltk.stem.snowball import SnowballStemmer
import re

# Sørg for at have hentet punkt-tokenizer, hvis nødvendigt
# import nltk
# nltk.download('punkt')


def load_transactions(folder_path, language='danish'):
    """
    Load all .txt files from the specified folder and treat each file as one transaction.
    Each word is stemmed using SnowballStemmer for the given language.
    Returns a list of transactions, where each transaction is a list of stemmed tokens.
    """
    stemmer = SnowballStemmer(language)
    transactions = []

    for filepath in glob.glob(os.path.join(folder_path, '*.txt')):
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

            # Fjern 'Prompt:' og 'Answer:' labels og metadata
            # Split på 'Answer:' for at fokusere på svarkomponenten
            parts = text.split('Answer:')
            content = parts[-1] if len(parts) > 1 else parts[0]

            # Normalisering: fjern alle non-alfanumeriske tegn, bortset fra mellemrum
            content = re.sub(r'[^\wæøåÆØÅ\s]', ' ', content)

            # Tokenisering på whitespace
            words = content.lower().split()

            # Stemming
            stems = [stemmer.stem(w) for w in words if w]
            transactions.append(stems)

    return transactions


def mine_association_rules(transactions, min_support=0.05, min_confidence=0.6):
    """
    Givet en liste af transaktioner (lister af tokens), beregn hyppige itemsets og tilhørende associationsregler.
    """
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # Frekvente itemsets
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)

    # Associationsregler
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    return frequent_itemsets, rules


if __name__ == '__main__':
    folder = 'output'
    print(f"Loading transactions from '{folder}'...")
    transactions = load_transactions(folder)
    print(f"Loaded {len(transactions)} transactions.")

    # Juster thresholds efter behov
    min_support = 0.05  # fx 5%
    min_confidence = 0.6  # fx 60%

    print(f"Mining association rules with support>={min_support} and confidence>={min_confidence}...")
    frequent_itemsets, rules = mine_association_rules(transactions, min_support, min_confidence)

    print("Frequent itemsets:")
    print(frequent_itemsets)
    print("\nAssociation Rules:")
    print(rules)