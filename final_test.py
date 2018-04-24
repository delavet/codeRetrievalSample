from gensim import models, similarities
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from my_corpuses import c_dictionary, t_dictionary, p_dictionary
import linecache
import sys
import warnings


warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
trained_model = 'trained_LDA_model.model'
trained_index = 'trained_LDA_index.index'
tfidf_model = 'tfidf_for_LDA.model'
tfidf_index = similarities.MatrixSimilarity.load('trained_tfidf_for_LDA_index.index')
code_trained_model = 'code_trained_LDA_model.model'
code_trained_index = 'code_trained_LDA_index.index'
code_tfidf_model = 'code_tfidf_for_LDA.model'
code_tfidf_index = similarities.MatrixSimilarity.load('code_trained_tfidf_for_LDA_index.index')
title_trained_model = 'title_trained_LDA_model.model'
title_trained_index = 'title_trained_LDA_index.index'
title_tfidf_model = 'title_tfidf_for_LDA.model'
title_tfidf_index = similarities.MatrixSimilarity.load('title_trained_tfidf_for_LDA_index.index')
query = input("input query:")
result_file = open(query+".txt", 'w', encoding='utf-8')
sys.stdout = result_file

post_file = open('post', 'r', encoding='utf-8')
code_file = open('code', 'r', encoding='utf-8')
title_file = open('title', 'r', encoding='utf-8')

stemmed_file = open('preprocessed', 'r', encoding='utf-8')
stopwords_file = open('unigram_stops', 'r', encoding='utf-8')
code_stemmed_file = open('code_preprocessed', 'r', encoding='utf-8')
code_stopwords_file = open('code_unigram_stops', 'r', encoding='utf-8')
title_stemmed_file = open('title_preprocessed', 'r', encoding='utf-8')
title_stopwords_file = open('title_unigram_stops', 'r', encoding='utf-8')

preprocessed_file = open('preprocessed', 'r', encoding='utf-8')
code_preprocessed_file = open('code_preprocessed', 'r', encoding='utf-8')
title_preprocessed_file = open('title_preprocessed', 'r', encoding='utf-8')
dictionary = p_dictionary
code_dictionary = c_dictionary
title_dictionary = t_dictionary

lda = models.LdaModel.load(trained_model)
index = similarities.MatrixSimilarity.load(trained_index)
tfidf = models.TfidfModel.load(tfidf_model)
code_lda = models.LdaModel.load(code_trained_model)
code_index = similarities.MatrixSimilarity.load(code_trained_index)
code_tfidf = models.TfidfModel.load(code_tfidf_model)
title_lda = models.LdaModel.load(title_trained_model)
title_index = similarities.MatrixSimilarity.load(title_trained_index)
title_tfidf = models.TfidfModel.load(title_tfidf_model)

q_tokenized = [word.lower() for word in word_tokenize(query)]
english_stopwords = [word.strip('\n') for word in stopwords_file]
q_stemmed = []
st = PorterStemmer()
for word in q_tokenized:
    is_soy = True
    for i in range(len(word)):
        if word[i].isalpha():
            is_soy = False
    if not is_soy:
        q_stemmed.append(st.stem(word))
q_filterer_stop = [word for word in q_stemmed if word not in english_stopwords]
print(q_filterer_stop)
q_bow = dictionary.doc2bow(q_filterer_stop)
code_q_bow = code_dictionary.doc2bow(q_filterer_stop)
title_q_bow = title_dictionary.doc2bow(q_filterer_stop)


q_lda = lda[q_bow]
q_tfidf = tfidf[q_bow]
code_q_lda = code_lda[code_q_bow]
code_q_tfidf = code_tfidf[code_q_bow]
title_q_lda = title_lda[title_q_bow]
title_q_tfidf = title_tfidf[title_q_bow]

tfidf_sims = tfidf_index[q_tfidf]
lda_sims = index[q_lda]
code_tfidf_sims = code_tfidf_index[code_q_tfidf]
code_lda_sims = code_index[code_q_lda]
title_tfidf_sims = title_tfidf_index[title_q_tfidf]
title_lda_sims = title_index[title_q_lda]


filtered_num = [sim[0] for sim in enumerate(code_lda_sims) if sim[1] <= 0.7]
sims = []
pure_lda_sims = []
pure_tfidf_sims = []

for i in range(len(tfidf_sims)):
    a = code_tfidf_sims[i]
    b = tfidf_sims[i]
    c = title_tfidf_sims[i]
    if a < 0.5 and b > 0.7:
        b = 0.7
    pure_tfidf_sims.append((i, 2*a+b+4*c))

sorted_pure_tfidf_sims = sorted(pure_tfidf_sims, key=lambda item: -item[1])

for i in range(len(tfidf_sims)):
    a = code_lda_sims[i]
    b = lda_sims[i]
    c = title_lda_sims[i]
    if a < 0.5 and b > 0.7:
        b = 0.7
    pure_lda_sims.append((i, a+b+c))

sorted_pure_lda_sims = sorted(pure_lda_sims, key=lambda item: -item[1])


for num in filtered_num:
    tfidf_sims[num] = 0.0
    lda_sims[num] = 0.0
    code_tfidf_sims[num] = 0.0
    title_tfidf_sims[num] = 0.0

for i in range(len(tfidf_sims)):
    a = code_tfidf_sims[i]
    b = tfidf_sims[i]
    c = title_tfidf_sims[i]
    if a < 0.5 and b > 0.7:
        b = 0.7
    sims.append((i, 2*a+b+c))
sorted_sims = sorted(sims, key=lambda item: -item[1])

print("my method")
i = 0
for result in sorted_sims:
    if(len(linecache.getline('code', result[0]+1)) < 20):
        continue
    i = i + 1
    if(i > 10):
        break
    print('result NO.' + str(i))
    print('code tfidf sim: ' + str(code_tfidf_sims[result[0]]))
    print('post tfidf sim: ' + str(tfidf_sims[result[0]]))
    print('title tfidf sim:' + str(title_lda_sims[result[0]]))
    print('code lda sim: ' + str(code_lda_sims[result[0]]))
    print('post lda sim: ' + str(lda_sims[result[0]]))
    print('title lda sim: ' + str(title_lda_sims[result[0]]))
    print('title content:')
    print(linecache.getline('title', result[0]+1))
    print('code content:')
    print(linecache.getline('code', result[0]+1))
    print('post content:')
    print(linecache.getline('post', result[0]+1))

print("pure_lda_sims")
i = 0
for result in sorted_pure_lda_sims:
    if(len(linecache.getline('code', result[0]+1)) < 20):
        continue
    i = i + 1
    if(i > 10):
        break
    print('result NO.' + str(i))
    print('code tfidf sim: ' + str(code_tfidf_sims[result[0]]))
    print('post tfidf sim: ' + str(tfidf_sims[result[0]]))
    print('title tfidf sim:' + str(title_lda_sims[result[0]]))
    print('code lda sim: ' + str(code_lda_sims[result[0]]))
    print('post lda sim: ' + str(lda_sims[result[0]]))
    print('title lda sim: ' + str(title_lda_sims[result[0]]))
    print('title content:')
    print(linecache.getline('title', result[0]+1))
    print('code content:')
    print(linecache.getline('code', result[0]+1))
    print('post content:')
    print(linecache.getline('post', result[0]+1))

print("pure_tfidf_sims")
i = 0
for result in sorted_sims:
    if(len(linecache.getline('code', result[0]+1)) < 20):
        continue
    i = i + 1
    if(i > 10):
        break
    print('result NO.' + str(i))
    print('code tfidf sim: ' + str(code_tfidf_sims[result[0]]))
    print('post tfidf sim: ' + str(tfidf_sims[result[0]]))
    print('title tfidf sim:' + str(title_lda_sims[result[0]]))
    print('code lda sim: ' + str(code_lda_sims[result[0]]))
    print('post lda sim: ' + str(lda_sims[result[0]]))
    print('title lda sim: ' + str(title_lda_sims[result[0]]))
    print('title content:')
    print(linecache.getline('title', result[0]+1))
    print('code content:')
    print(linecache.getline('code', result[0]+1))
    print('post content:')
    print(linecache.getline('post', result[0]+1))
preprocessed_file.close()
code_file.close()
post_file.close()
title_file.close()
result_file.close()
