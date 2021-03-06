"""En este script se desarrolla el preprocesamiento, es decir, se pasa del
dataset crudo a una forma de array que pueda procesarse por las herramientas
de predicción.

Esencialmente, se espera de este archivo dos variables, datarray y datarget,
que deben ser arrays de numpy, la primera de dos dimensiones, con cada row
representando una entrada del dataset con sus respectivos atributos, y datarget
debe ser unidimensional, conteniendo la etiqueta real de cada punto de datos.

Autor: Roque del Río
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import xml.etree.ElementTree as ET
import datetime

analyser = SentimentIntensityAnalyzer()
Translator = Translator()

# get XML files
def get_files(master):
    task_n = sum(1 for line in open("./pan19_author_profiling_training_es/" + master + ".txt"))
    task_nc = 0
    dfset = []
    with open("./pan19_author_profiling_training_es/" + master + ".txt", 'r+' ,encoding="utf-8") as file:
        for line in file:
            entry = line.split(':::')
            author = entry[0]
            botvalue = entry[1]
            entrydict = build_dict(author)
            if botvalue == 'bot':
                entrydict.update({"botvalue": 1})
            dfset.append(entrydict)

            datetime_object = str(datetime.datetime.now())
            task_nc += 1
            print('[' + datetime_object + '] finished task ' + str(task_nc) + ' of ' + str(task_n))
    return dfset

def build_dict(author):
    file = "./pan19_author_profiling_training_es/" + author + ".xml"

    # XML stuff
    tree = ET.parse(file)
    root = tree.getroot()

    #NLP stuff


    rts = 0
    links = 0
    punctuation = 0
    hashtags = 0
    tags = 0

    positive = 0
    neutral = 0
    negative = 0
    compound = 0

    suspicious_words = 0
    suspicious_words_lsit = ["bot", "bots", "sigueme", "sigame", "seguidores", 
                             "empleoTIC", "empleoTICJOB", "SEGUIDORES", "SIGUES", 
                             "Follow", "OBSERVADOR", "DESCARGAR", "ipautaorg", "hacerfotos",
                            "Unete", "ccdBot", "VIDEO", "elpaisuy", "ad", "cp", "TrafficBotGT"
                            "AJNews", "Venta", "iPhone"]

    for entry in root.iter('document'):
        text = entry.text

        # suspicious words
        text_split = entry.text.split()
        for word in text_split:
            if word in suspicious_words_lsit:
                suspicious_words += 1

        # Sentiment
        #text_trans = Translator.translate(text=text, src='es', dest='en')
        score = analyser.polarity_scores(text)
        positive += score['pos']
        neutral += score['neu']
        negative += score['neg']
        compound += score['compound']

        # RT
        rts += text.count('RT @')
        # Link
        links += text.count('http://')
        links += text.count('https://')
        # Punct
        punctuation += text.count('. ')
        punctuation += text.count(', ')
        punctuation += text.count('; ')
        # hashtags
        hashtags += text.count('#')
        # tags
        tags += text.count('@')

    entrydict = {
        "author" : author,
        "rts" : rts,
        "links" : links,
        "punctuation" : punctuation,
        "hashtags" : hashtags,
        "tags" : tags,
        "botvalue" : 0,
        "positive" : positive,
        "neutral": neutral,
        "negative": negative,
        "compound": compound,
        "suspicious_words": suspicious_words
    }

    return entrydict
