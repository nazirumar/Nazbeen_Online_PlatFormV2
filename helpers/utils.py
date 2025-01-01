# import nltk
# from spellchecker import SpellChecker
# from langdetect import detect
# from nltk.corpus import wordnet
# from googletrans import Translator


# # Initialize SpellChecker
# spell = SpellChecker()

# # Initialize Google Translator
# translator = Translator()

# def preprocess_query(query):
#     """
#     Preprocess the user query: spelling correction, query expansion, language detection, and normalization.
#     """
#     # Normalize text (lowercase, remove special characters)
#     query = query.lower().strip()

#     # Spell Correction
#     corrected_query = " ".join([spell.correction(word) for word in query.split()])

#     # Query Expansion using WordNet
#     expanded_query = expand_query_with_synonyms(corrected_query)

#     # Detect Language
#     language = detect(expanded_query)
#     if language != 'en':
#         # If non-English, translate to English
#         print(f"Detected language: {language}. Attempting translation...")
#         expanded_query = translator.translate(expanded_query, src=language, dest='en').text

#     return expanded_query

# def expand_query_with_synonyms(query):
#     """
#     Expand the query with synonyms using WordNet to improve search relevance.
#     """
#     words = query.split()
#     expanded_query = []

#     for word in words:
#         # Get synonyms from WordNet
#         synonyms = set()
#         for syn in wordnet.synsets(word):
#             for lemma in syn.lemmas():
#                 synonyms.add(lemma.name())

#         # Replace word with synonym if any, otherwise keep original word
#         if synonyms:
#             expanded_query.append(synonyms.pop())  # Take the first synonym
#         else:
#             expanded_query.append(word)

#     return " ".join(expanded_query)
