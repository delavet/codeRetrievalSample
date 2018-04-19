from gensim import corpora, models
from sklearn import preprocessing

import scipy.stats
from numpy import linalg
from code_lda_train import MyCodeCorpus
from LDAtrain import MyCorpus
from title_LDAtrain import MyTitleCorpus
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

post_name = 'preprocessed'
title_name = 'title_preprocessed'
code_name = 'code_preprocessed'
measure_file = open('measure', 'w', encoding='utf-8')


def my_cmp(x, y):
    return y - x


def test_topic_num(topic_num, name):
    preprocessed_file = open(name, 'r', encoding='utf-8')
    texts = [line.strip('\n').split(',') for line in preprocessed_file]
    dictionary = corpora.Dictionary(texts)
    L = [len(text) for text in texts]
    corpus = None
    if name == post_name:
        corpus = MyCorpus()
    elif name == title_name:
        corpus = MyTitleCorpus()
    else:
        corpus = MyCodeCorpus()
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
    preprocessed_file.close()


def real_test(name):
    for num in range(10, 150):
        test_topic_num(num, name)


i = input('train what?t p or c?')
if i == 't':
    real_test(title_name)
elif i == 'p':
    real_test(post_name)
else:
    real_test(code_name)
measure_file.close()
print('done')
