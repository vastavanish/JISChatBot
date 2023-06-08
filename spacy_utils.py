import spacy
import numpy as np


nlp = spacy.load("en_core_web_sm")

# sentence = "There's is Anish!"


jis_stopwords = ['name','namely']

for stopword in jis_stopwords:
    nlp.Defaults.stop_words.remove(stopword)


def preprocess_input_sentence(sentence: str):
    '''
    sentence : str input string
    returns :
    tokenized_list, lemmatized_list, stopword_removal_list

    '''

    doc = nlp(sentence)

    

    tokenized_list = [token for token in doc if not token.is_punct]


    stopword_removal_list = [
        token for token in tokenized_list if not token.is_stop]



    lemmatized_list = [token.lemma_.lower()
                       for token in stopword_removal_list if token.is_alpha]



    return tokenized_list, lemmatized_list, stopword_removal_list


# print(preprocess_input_sentence("There's is Anish!"))


def bag_of_words(tokenized_sentence, vocabulary):
    '''
    sentence = ["Hello", "How", "are", "you"]
    words = ["hi", "hello", "I", "you", "thank", "cool"]
    bag = [    0  ,  1    ,  0   ,1    ,   0    ,   0  ]

    '''

    bag = np.zeros(len(vocabulary), dtype=np.float32)

    for idx, w in enumerate(vocabulary):
        if w in tokenized_sentence:
            bag[idx] = 1.0

    return bag
