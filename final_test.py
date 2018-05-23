from gensim import corpora, models, similarities
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import linecache
import sys
import warnings


warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
cat = input("which model do you want to use?") + '/'
t_dictionary = corpora.Dictionary.load(cat+"t_dict.dict")
p_dictionary = corpora.Dictionary.load(cat+"p_dict.dict")
c_dictionary = corpora.Dictionary.load(cat+"c_dict.dict")
trained_model = cat + 'trained_LDA_model.model'
trained_index = cat + 'trained_LDA_index.index'
tfidf_model = cat + 'tfidf_for_LDA.model'

code_trained_model = cat + 'code_trained_LDA_model.model'
code_trained_index = cat + 'code_trained_LDA_index.index'
code_tfidf_model = cat + 'code_tfidf_for_LDA.model'

title_trained_model = cat + 'title_trained_LDA_model.model'
title_trained_index = cat + 'title_trained_LDA_index.index'
title_tfidf_model = cat + 'title_tfidf_for_LDA.model'

query = input("input query:")
result_file = open(query+".txt", 'w', encoding='utf-8')
sys.stdout = result_file

id_file = open(cat + 'id', 'r', encoding='utf-8')
post_file = open(cat + 'post', 'r', encoding='utf-8')
code_file = open(cat + 'code', 'r', encoding='utf-8')
title_file = open(cat + 'title', 'r', encoding='utf-8')

stemmed_file = open(cat + 'preprocessed', 'r', encoding='utf-8')
stopwords_file = open(cat + 'unigram_stops', 'r', encoding='utf-8')
code_stemmed_file = open(cat + 'code_preprocessed', 'r', encoding='utf-8')
code_stopwords_file = open(cat + 'code_unigram_stops', 'r', encoding='utf-8')
title_stemmed_file = open(cat + 'title_preprocessed', 'r', encoding='utf-8')
title_stopwords_file = open(cat + 'title_unigram_stops', 'r', encoding='utf-8')

preprocessed_file = open(cat + 'preprocessed', 'r', encoding='utf-8')
code_preprocessed_file = open(cat + 'code_preprocessed', 'r', encoding='utf-8')
title_preprocessed_file = open(cat + 'title_preprocessed', 'r', encoding='utf-8')
dictionary = p_dictionary
code_dictionary = c_dictionary
title_dictionary = t_dictionary

lda = models.LdaModel.load(trained_model)

tfidf = models.TfidfModel.load(tfidf_model)
code_lda = models.LdaModel.load(code_trained_model)

code_tfidf = models.TfidfModel.load(code_tfidf_model)
title_lda = models.LdaModel.load(title_trained_model)

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

tfidf_index = similarities.MatrixSimilarity.load(cat + 'trained_tfidf_for_LDA_index.index')
tfidf_sims = tfidf_index[q_tfidf]
del tfidf_index
index = similarities.MatrixSimilarity.load(trained_index)
lda_sims = index[q_lda]
del index
code_tfidf_index = similarities.MatrixSimilarity.load(cat + 'code_trained_tfidf_for_LDA_index.index')
code_tfidf_sims = code_tfidf_index[code_q_tfidf]
del code_tfidf_index
code_index = similarities.MatrixSimilarity.load(code_trained_index)
code_lda_sims = code_index[code_q_lda]
del code_index
title_tfidf_index = similarities.MatrixSimilarity.load(cat + 'title_trained_tfidf_for_LDA_index.index')
title_tfidf_sims = title_tfidf_index[title_q_tfidf]
del title_tfidf_index
title_index = similarities.MatrixSimilarity.load(title_trained_index)
title_lda_sims = title_index[title_q_lda]
del title_index


filtered_num = [sim[0] for sim in enumerate(code_lda_sims) if sim[1] <= 0.7]
sims = []
pure_lda_sims = []
pure_tfidf_sims = []
print("len of tfidf_sims"+str(len(tfidf_sims)))

for i in range(len(tfidf_sims)):
    a = code_tfidf_sims[i]
    b = tfidf_sims[i]
    c = title_tfidf_sims[i]
    if a < 0.5 and b > 0.8:
        b = 0.8
    pure_tfidf_sims.append((i, 2*a+b+4*c))

sorted_pure_tfidf_sims = sorted(pure_tfidf_sims, key=lambda item: -item[1])

for i in range(len(tfidf_sims)):
    a = code_lda_sims[i]
    b = lda_sims[i]
    c = title_lda_sims[i]
    if a < 0.5 and b > 0.8:
        b = 0.8
    pure_lda_sims.append((i, a+b+c))

sorted_pure_lda_sims = sorted(pure_lda_sims, key=lambda item: -item[1])


for num in filtered_num:
    tfidf_sims[num] = 0.0
    code_tfidf_sims[num] = 0.0
    title_tfidf_sims[num] = 0.0

for i in range(len(tfidf_sims)):
    a = code_tfidf_sims[i]
    b = tfidf_sims[i]
    c = title_tfidf_sims[i]
    if a < 0.5 and b > 0.8:
        b = 0.8
    sims.append((i, 2*a+b+4*c))
sorted_sims = sorted(sims, key=lambda item: -item[1])

print("my method")
i = 0
for result in sorted_sims:
    if(len(linecache.getline(cat + 'code', result[0]+1)) < 20):
        continue
    i = i + 1
    if(i > 5):
        break
    print('result NO.' + str(i) + '\n')
    print('code tfidf sim: ' + str(code_tfidf_sims[result[0]]))
    print('post tfidf sim: ' + str(tfidf_sims[result[0]]))
    print('title tfidf sim:' + str(title_lda_sims[result[0]]))
    print('code lda sim: ' + str(code_lda_sims[result[0]]))
    print('post lda sim: ' + str(lda_sims[result[0]]))
    print('title lda sim: ' + str(title_lda_sims[result[0]]))
    print('id:')
    print(linecache.getline(cat + 'id', result[0]+1))
    print('title content:')
    print(linecache.getline(cat + 'title', result[0]+1))
    print('code content:')
    print(linecache.getline(cat + 'code', result[0]+1).replace('\t', '\n'))
    print('post content:')
    print(linecache.getline(cat + 'post', result[0]+1))

print("pure_lda_sims")
i = 0
for result in sorted_pure_lda_sims:
    if(len(linecache.getline(cat + 'code', result[0]+1)) < 20):
        continue
    i = i + 1
    if(i > 5):
        break
    print('result NO.' + str(i) + '\n')
    print('code tfidf sim: ' + str(code_tfidf_sims[result[0]]))
    print('post tfidf sim: ' + str(tfidf_sims[result[0]]))
    print('title tfidf sim:' + str(title_lda_sims[result[0]]))
    print('code lda sim: ' + str(code_lda_sims[result[0]]))
    print('post lda sim: ' + str(lda_sims[result[0]]))
    print('title lda sim: ' + str(title_lda_sims[result[0]]))
    print('id:')
    print(linecache.getline(cat + 'id', result[0]+1))
    print('title content:')
    print(linecache.getline(cat + 'title', result[0]+1))
    print('code content:')
    print(linecache.getline(cat + 'code', result[0]+1).replace('\t', '\n'))
    print('post content:')
    print(linecache.getline(cat + 'post', result[0]+1))

print("pure_tfidf_sims")
i = 0
for result in sorted_pure_tfidf_sims:
    if(len(linecache.getline(cat + 'code', result[0]+1)) < 20):
        continue
    i = i + 1
    if(i > 5):
        break
    print('result NO.' + str(i) + '\n')
    print('code tfidf sim: ' + str(code_tfidf_sims[result[0]]))
    print('post tfidf sim: ' + str(tfidf_sims[result[0]]))
    print('title tfidf sim:' + str(title_lda_sims[result[0]]))
    print('code lda sim: ' + str(code_lda_sims[result[0]]))
    print('post lda sim: ' + str(lda_sims[result[0]]))
    print('title lda sim: ' + str(title_lda_sims[result[0]]))
    print('id:')
    print(linecache.getline(cat + 'id', result[0]+1))
    print('title content:')
    print(linecache.getline(cat + 'title', result[0]+1))
    print('code content:')
    print(linecache.getline(cat + 'code', result[0]+1).replace('\t', '\n'))
    print('post content:')
    print(linecache.getline(cat + 'post', result[0]+1))
preprocessed_file.close()
code_file.close()
post_file.close()
title_file.close()
result_file.close()
