from gensim import corpora, models, similarities
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from pprint import pprint
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
trained_model = 'code_trained_LDA_model.model'
trained_index = 'code_trained_LDA_index.index'
tfidf_model = 'code_tfidf_for_LDA.model'
query = "blur image swing"

post_file = open('post', 'r', encoding='utf-8')
code_file = open('code', 'r', encoding='utf-8')
stemmed_file = open('code_preprocessed', 'r', encoding='utf-8')
stopwords_file = open('code_unigram_stops', 'r', encoding='utf-8')
post_lines = post_file.readlines()
code_lines = code_file.readlines()
stemmed_lines = stemmed_file.readlines()
preprocessed_file = open('code_preprocessed', 'r', encoding='utf-8')
dictionary = corpora.Dictionary(line.strip('\n').split(',') for line in preprocessed_file)

lda = models.LdaModel.load(trained_model)
index = similarities.MatrixSimilarity.load(trained_index)
tfidf_index = similarities.MatrixSimilarity.load('code_trained_tfidf_for_LDA_index.index')

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
q_lda = lda[q_bow]
q_tfidf = tfidf[q_bow]
print(q_lda)

sims = tfidf_index[q_tfidf]
lda_sims = index[q_lda]
sorted_sims = sorted(enumerate(sims), key=lambda item: -item[1])
filtered_lda_num = [sim[0] for sim in enumerate(lda_sims) if sim[1] > 0.7]
filtered_sims = [sim for sim in sorted_sims if sim[0] in filtered_lda_num]
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
    print('\n')

preprocessed_file.close()
code_file.close()
post_file.close()
