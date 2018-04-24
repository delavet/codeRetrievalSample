import warnings
from gensim import models, similarities
from pprint import pprint
from my_corpuses import MyCorpus, p_dictionary
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

number = int(input("input topic num:"))


def train():
    corpus = MyCorpus()
    tfidf = models.TfidfModel(corpus)
    tfidf.save('tfidf_for_LDA.model')
    corpus_tfidf = tfidf[corpus]
    lda = models.LdaModel(corpus, id2word=p_dictionary, num_topics=number, iterations=8000)
    lda.save('trained_LDA_model.model')
    topics = lda.print_topics(num_topics=20, num_words=30)
    pprint(topics)
    index = similarities.MatrixSimilarity(lda[corpus])
    tf_idf_index = similarities.MatrixSimilarity(corpus_tfidf, num_features=len(p_dictionary.keys()))
    index.save('trained_LDA_index.index')
    tf_idf_index.save('trained_tfidf_for_LDA_index.index')
    print('trained!')


train()
