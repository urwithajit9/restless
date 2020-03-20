import nltk
import re
import string

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, LancasterStemmer, RegexpStemmer, SnowballStemmer
from nltk.stem import WordNetLemmatizer

default_stemmer = LancasterStemmer()
default_stopwords = stopwords.words("english")

default_lemmatizer = WordNetLemmatizer()


class TextNormalizer:
    """
    Tools for text pre-processing.
    """

    def __init__(self):
        self.wordnet_tags = {
            "J": wordnet.ADJ,
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "R": wordnet.ADV,
        }

    def tokenize_text(self, text: str):
        """
        Tokenizes text.
        """
        return [w for s in sent_tokenize(text) for w in word_tokenize(s)]

    def lemmatize_text(self, text: str, lemmatizer=default_lemmatizer):
        tokens = self.tokenize_text(text)
        if isinstance(default_lemmatizer, WordNetLemmatizer):
            return " ".join(
                [
                    lemmatizer.lemmatize(token, self._get_wordnet_pos(token))
                    for token in tokens
                ]
            )
        else:
            return " ".join([lemmatizer.lemmatize(token) for token in tokens])

    def stem_text(self, text: str, stemmer=default_stemmer):
        tokens = self.tokenize_text(text)
        return " ".join([stemmer.stem(t) for t in tokens])

    def remove_stopwords(self, text: str, stop_words=default_stopwords):
        tokens = [w for w in self.tokenize_text(text) if w not in stop_words]
        return " ".join(tokens)

    def strip_whitepsace(self, text: str):
        return text.strip()

    def lowercase_text(self, text: str):
        return text.lower()

    def strip_punctuation(self, text: str):
        return text.translate(str.maketrans("", "", string.punctuation))

    def _get_wordnet_pos(self, word: str, wordnet_tags: dict = None):
        """Map POS tag to first character lemmatize() accepts."""
        if wordnet_tags is None:
            wordnet_tags = self.wordnet_tags
        tag = nltk.pos_tag([word])[0][1][0].upper()
        return wordnet_tags.get(tag, wordnet.NOUN)  # noun by default

    def normalize_text(
        self,
        text: str,
        lowercase: bool = False,
        strip_punct: bool = False,
        strip_whitespace: bool = True,
        remove_stopwords: bool = False,
        lemmatize_text: bool = False,
        stem_text: bool = False,
    ):
        normalized_text = text
        if lowercase:
            # we don't want to lowercase by default, because capitalization means
            # different things (proper vs common noun); decreases doc2vec success
            normalized_text = self.lowercase_text(normalized_text)
        if strip_punct:
            # stripping punctuation also decreases doc2vec model accuracy
            normalized_text = self.strip_punctuation(normalized_text)
        if strip_whitespace:
            normalized_text = self.strip_whitepsace(normalized_text)
        if remove_stopwords:
            normalized_text = self.remove_stopwords(normalized_text)
        if stem_text:
            normalized_text = self.stem_text(normalized_text)
        if lemmatize_text:
            normalized_text = self.lemmatize_text(normalized_text)
        return normalized_text
