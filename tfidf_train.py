import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models, similarities

preprocessed_file = open('preprocessed', 'r', encoding='utf-8')
dictionary = corpora.Dictionary(line.strip('\n').split(',') for line in preprocessed_file)
preprocessed_file.close()
number = 10

texts = [line.strip('\n').split(',') for line in open('preprocessed', 'r', encoding='utf-8')]
print(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
print(corpus)
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
print(corpus_tfidf)
index = similarities.MatrixSimilarity(corpus_tfidf, num_features=len(dictionary.keys()))

tfidf.save('tfidf_trained.model')
index.save('tfidf_index.index')

print('trained!')

3540
