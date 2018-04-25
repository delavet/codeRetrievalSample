from gensim import models
from sklearn import preprocessing
import linecache
import util
import scipy.stats
from numpy import linalg
from my_corpuses import MyCodeCorpus, MyCorpus, MyTitleCorpus,  p_dictionary, c_dictionary, t_dictionary 
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

post_name = 'preprocessed'
title_name = 'title_preprocessed'
code_name = 'code_preprocessed'
measure_name = '_measure.csv'


def my_cmp(x, y):
    return y - x


def test_topic_num(topic_num, name, measure_file):
    corpus = None
    dictionary = None
    if name == post_name:
        corpus = MyCorpus()
        dictionary = p_dictionary
    elif name == title_name:
        corpus = MyTitleCorpus()
        dictionary = t_dictionary
    else:
        corpus = MyCodeCorpus()
        dictionary = c_dictionary
    L = []
    for line in open(name, encoding='utf-8'):
        L.append(len(line.strip('\n').split(',')))
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
    for i in range(util.file_len('L')):
        bow = dictionary.doc2bow(linecache.getline(name, i+1).strip('\n').split(','))
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
    write_str = str(topic_num) + ',' + str(measure) + '\n'
    measure_file.write(write_str)


def real_test(name):
    measure_f = open(name+measure_name, 'w', encoding='utf-8')
    measure_f.write('topic num,KL\n')
    for num in range(20, 92):
        if num % 2 == 0:
            print(str(num)+' detecting')
            test_topic_num(num, name, measure_f)
    measure_f.close()


i = input('train what?t p or c?')
if i == 't':
    print('detect a t!')
    real_test(title_name)
elif i == 'p':
    print('detect a p!')
    real_test(post_name)
else:
    print('detect a c!')
    real_test(code_name)
print('done')
