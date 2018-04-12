from gensim import corpora, models, similarities
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
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
query = input("input query:")

post_file = open('post', 'r', encoding='utf-8')
code_file = open('code', 'r', encoding='utf-8')
stemmed_file = open('preprocessed', 'r', encoding='utf-8')
stopwords_file = open('unigram_stops', 'r', encoding='utf-8')
code_stemmed_file = open('code_preprocessed', 'r', encoding='utf-8')
code_stopwords_file = open('code_unigram_stops', 'r', encoding='utf-8')
post_lines = post_file.readlines()
code_lines = code_file.readlines()
stemmed_lines = stemmed_file.readlines()
preprocessed_file = open('preprocessed', 'r', encoding='utf-8')
code_preprocessed_file = open('code_preprocessed', 'r', encoding='utf-8')
dictionary = corpora.Dictionary(line.strip('\n').split(',') for line in preprocessed_file)
code_dictionary = corpora.Dictionary(line.strip('\n').split(',') for line in code_preprocessed_file)

lda = models.LdaModel.load(trained_model)
index = similarities.MatrixSimilarity.load(trained_index)
tfidf = models.TfidfModel.load(tfidf_model)
code_lda = models.LdaModel.load(code_trained_model)
code_index = similarities.MatrixSimilarity.load(code_trained_index)
code_tfidf = models.TfidfModel.load(code_tfidf_model)

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


q_lda = lda[q_bow]
q_tfidf = tfidf[q_bow]
code_q_lda = code_lda[code_q_bow]
code_q_tfidf = code_tfidf[code_q_bow]

tfidf_sims = tfidf_index[q_tfidf]
lda_sims = index[q_lda]
code_tfidf_sims = code_tfidf_index[code_q_tfidf]
code_lda_sims = code_index[code_q_lda]


filtered_num = [sim[0] for sim in enumerate(code_lda_sims) if sim[1] <= 0.7]
sims = []
'''
for num in filtered_num:
    tfidf_sims[num] = 0.0
    lda_sims[num] = 0.0
    code_tfidf_sims[num] = 0.0
'''
for i in range(len(tfidf_sims)):
    a = code_tfidf_sims[i]
    b = tfidf_sims[i]
    if a < 0.5 and b > 0.7:
        b = 0.7
    sims.append((i, a+b))
sorted_sims = sorted(sims, key=lambda item: -item[1])

i = 0
for result in sorted_sims:
    if(len(code_lines[result[0]]) < 20):
        continue
    i = i + 1
    if(i > 10):
        break
    print('result NO.' + str(i))
    print('code tfidf sim: ' + str(code_tfidf_sims[result[0]]))
    print('post tfidf sim: ' + str(tfidf_sims[result[0]]))
    print('code lda sim: ' + str(code_lda_sims[result[0]]))
    print('post lda sim: ' + str(lda_sims[result[0]]))
    print('code content:')
    print(code_lines[result[0]])
    print('post content:')
    print(post_lines[result[0]])
preprocessed_file.close()
code_file.close()
post_file.close()
