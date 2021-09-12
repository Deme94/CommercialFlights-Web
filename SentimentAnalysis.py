# import goslate
import re
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
    try:
        newPhrase=phrase
        translator = Translator()
        translated = translator.translate(newPhrase)
        texto = translated.text
        texto = re.sub('\W',texto)
        return texto
    except:
        return "Not bad"

def analizar_string(phrase):
    """  vader """
    try:
        analyser = SentimentIntensityAnalyzer()
        score = analyser.polarity_scores(phrase)
        return score['compound']
    except:
        return 0
