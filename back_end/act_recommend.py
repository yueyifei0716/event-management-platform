import re
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer
from statistics import mean
import numpy
# import nltk
# nltk.download('punkt')


def sort_index(lst, rev=False):
    index = range(len(lst))
    s = sorted(index, reverse=rev, key=lambda i: lst[i])
    return s

def remove_punctuations(sentence):
    return re.sub(r'[^\w\s]', '', sentence.lower())

def clean_text(text):
    """
    This function takes as input a text on which several
    NLTK algorithms will be applied in order to preprocess it
    """
    tokens = word_tokenize(text)
    # Remove the punctuations
    tokens = [word for word in tokens if word.isalpha()]
    # Lower the tokens
    tokens = [word.lower() for word in tokens]
    # Remove stopword
    tokens = [word for word in tokens if not word in stopwords.words("english")]
    # Lemmatize
    lemma = WordNetLemmatizer()
    tokens = [lemma.lemmatize(word, pos = "v") for word in tokens]
    tokens = [lemma.lemmatize(word, pos = "n") for word in tokens]
    return set(tokens)

def text_similarity(text1, text2):
    l1 = []
    l2 = []
    # form a set containing keywords of both strings
    rvector = text1.union(text2)
    for w in rvector:
        if w in text1: l1.append(1) # create a vector
        else: l1.append(0)
        if w in text2: l2.append(1)
        else: l2.append(0)
    c = 0

    # cosine formula
    for i in range(len(rvector)):
        c+= l1[i]*l2[i]
            
    if float((sum(l1)*sum(l2))**0.5) == 0:
        return 0
    cosine = c / float((sum(l1)*sum(l2))**0.5)
    return cosine

def recommendation_top5(booked_acts, other_acts):
    # using the cosine similarity to calculate the similarity
    # between the booked_acts and other_acts
    docs_num = len(other_acts)
    print(docs_num)
    if docs_num == 0:
        return []
    sm = [None for x in range(len(booked_acts))]
    marks = [0 for x in range(len(other_acts))]
    for i, booked_act in enumerate(booked_acts):
        for j, other_act in enumerate(other_acts):
            similarity = text_similarity(clean_text(booked_act['description']), clean_text(other_act['description']))
            marks[j] = similarity
        sm[i] = marks.copy()
    print(sm)

    res = numpy.array([mean(x) for x in zip(*sm)])
    sort_index = numpy.argsort(res)[::-1]
    print(res)
    if docs_num <= 5:
        indexs = sort_index
    else:
        indexs = sort_index[:5]
    print("indexs: ", indexs)
    recommend_docs = [other_acts[index] for index in indexs]
    print(recommend_docs)
    recommend_ids = [doc['id'] for doc in recommend_docs]
    return recommend_ids


