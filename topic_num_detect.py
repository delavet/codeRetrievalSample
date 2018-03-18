import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models, similarities
from sklearn import preprocessing
from pprint import pprint

import numpy as np
import scipy.stats
from numpy import linalg
from LDAtrain import MyCorpus
preprocessed_file = open('preprocessed', 'r', encoding='utf-8')
measure_file = open('measure', 'w', encoding='utf-8')
texts = [line.strip('\n').split(',') for line in preprocessed_file]
dictionary = corpora.Dictionary(texts)
L = [len(text) for text in texts]
preprocessed_file.close()


def my_cmp(x,y):
    return y - x


def test_topic_num(topic_num):
    corpus = MyCorpus()
    lda = models.LdaModel(corpus, id2word=dictionary, num_topics=topic_num, iterations=4000)
    M1 = lda.get_topics()
    u, m1_sigma, vh = linalg.svd(M1)
    m1_sigma_list = m1_sigma.tolist()
    print(m1_sigma_list)
    temp = []
    temp.append(m1_sigma_list)
    cm1_a = preprocessing.normalize(temp, norm='l1')[0]
    cm1 = sorted(cm1_a, reverse=True)
    print(cm1)
    cm2_unorm = []
    for i in range(topic_num):
        cm2_unorm.append(0)
    for i in range(len(texts)):
        bow = dictionary.doc2bow(texts[i])
        m2_vec = lda.get_document_topics(bow)
        for tp in m2_vec:
            cm2_unorm[tp[0]] = cm2_unorm[tp[0]] + L[i]*tp[1]
    print(cm2_unorm)
    temp = [cm2_unorm]
    cm2_a = preprocessing.normalize(temp, norm='l1')[0]
    cm2 = sorted(cm2_a, reverse=True)
    print(cm2)
    KL1 = scipy.stats.entropy(cm1, cm2)
    KL2 = scipy.stats.entropy(cm2, cm1)
    measure = KL1 + KL2
    write_str = str(topic_num) + ':' + str(measure) + '\n'
    measure_file.write(write_str)


numbers = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150]
for num in numbers:
    test_topic_num(num)
measure_file.close()

