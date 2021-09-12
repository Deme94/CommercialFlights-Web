#import goslate
import time
from googletrans import Translator

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Libreria goslate
"""def detectAndTransalateFailed(phrase):
    newPhrase = phrase
    translator = Translator(to_lang="en")
    translated = translator.translate(newPhrase)

    return translated
"""
"""
def detectAndTransalate(phrase):
    text = phrase
    gs = goslate.Goslate()
    translatedText = gs.translate(text, 'en')

    return translatedText
"""

# Librería googletrans
def detectAndTransalate(phrase):
    newPhrase = phrase
    translator = Translator(to_lang="en")
    translated = translator.translate(newPhrase)
    time.sleep(5)
    return translated

def analizar_string(phrase):
    """  vader """
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(phrase)
    return score['compound']
