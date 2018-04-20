import warnings
from gensim import models, similarities
from pprint import pprint
from my_corpuses import MyTitleCorpus, t_dictionary
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

number = 49


def train():
    corpus = MyTitleCorpus()
    tfidf = models.TfidfModel(corpus)
    tfidf.save('title_tfidf_for_LDA.model')
    corpus_tfidf = tfidf[corpus]
    lda = models.LdaModel(corpus, id2word=t_dictionary, num_topics=number, iterations=8000)
    lda.save('title_trained_LDA_model.model')
    topics = lda.print_topics(num_topics=20, num_words=30)
    pprint(topics)
    index = similarities.MatrixSimilarity(lda[corpus])
    tf_idf_index = similarities.MatrixSimilarity(corpus_tfidf, num_features=len(t_dictionary.keys()))
    index.save('title_trained_LDA_index.index')
    tf_idf_index.save('title_trained_tfidf_for_LDA_index.index')
    print('trained!')


train()
