import warnings
from gensim import models, similarities
from pprint import pprint
from my_corpuses import MyCodeCorpus, c_dictionary
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

number = 20


def train():
    corpus = MyCodeCorpus()
    tfidf = models.TfidfModel(corpus)
    tfidf.save('code_tfidf_for_LDA.model')
    corpus_tfidf = tfidf[corpus]
    lda = models.LdaModel(corpus, id2word=c_dictionary, num_topics=number, iterations=8000)
    lda.save('code_trained_LDA_model.model')
    topics = lda.print_topics(num_topics=20, num_words=30)
    pprint(topics)
    index = similarities.MatrixSimilarity(lda[corpus])
    tf_idf_index = similarities.MatrixSimilarity(corpus_tfidf, num_features=len(c_dictionary.keys()))
    index.save('code_trained_LDA_index.index')
    tf_idf_index.save('code_trained_tfidf_for_LDA_index.index')
    print('trained!')


train()
