from gensim import corpora, models, similarities
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from pprint import pprint
import warnings
trained_model = 'trained_LDA_model.model'
trained_index = 'trained_LDA_index.index'
tfidf_model = 'tfidf_for_LDA.model'
query = "select max max value from array"
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
post_file = open('post', 'r', encoding='utf-8')
code_file = open('code', 'r', encoding='utf-8')
stemmed_file = open('preprocessed', 'r', encoding='utf-8')
stopwords_file = open('unigram_stops', 'r', encoding='utf-8')
post_lines = post_file.readlines()
code_lines = code_file.readlines()
stemmed_lines = stemmed_file.readlines()
preprocessed_file = open('preprocessed', 'r', encoding='utf-8')
dictionary = corpora.Dictionary(line.strip('\n').split(',') for line in preprocessed_file)

lda = models.LdaModel.load(trained_model)
index = similarities.MatrixSimilarity.load(trained_index)
tfidf = models.TfidfModel.load(tfidf_model)

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

print(q_bow)
q_tfidf = tfidf[q_bow]
print(q_tfidf)
q_lda = lda[q_tfidf]
print(q_lda)

sims = index[q_lda]
sorted_sims = sorted(enumerate(sims), key=lambda item: -item[1])
i = 0
for result in sorted_sims:
    if(len(code_lines[result[0]]) < 20):
        continue
    i = i + 1
    if(i > 10):
        break
    print('result NO.' + str(i))
    print('code content:')
    pprint(code_lines[result[0]])
    print('post content:')
    pprint(post_lines[result[0]])
    stemmed = stemmed_lines[result[0]]
    ans_doc2bow = dictionary.doc2bow(stemmed.strip('\n').split(','))
    print('doc2bow:')
    pprint(ans_doc2bow)
    ans_tfidf = tfidf[ans_doc2bow]
    print('tfidf:')
    pprint(ans_tfidf)
    ans_lda = lda[ans_tfidf]
    print('lda:')
    pprint(ans_lda)
    print('\n')

preprocessed_file.close()
code_file.close()
post_file.close()
