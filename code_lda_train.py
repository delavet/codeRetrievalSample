import warnings
from gensim import corpora, models, similarities
from pprint import pprint
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

preprocessed_file = open('code_preprocessed', 'r', encoding='utf-8')
texts = [line.strip('\n').split(',') for line in preprocessed_file]
dictionary = corpora.Dictionary(texts)

number = 20


class MyCodeCorpus(object):
    def __iter__(self):
        for line in open('code_preprocessed', encoding='utf-8'):
            yield dictionary.doc2bow(line.strip('\n').split(','))

    def __len__(self):
        count = 0
        the_file = open('code_preprocessed', encoding='utf-8')
        while True:
            buffer = the_file.read(1024 * 8192)
            if not buffer:
                break
            count += buffer.count('\n')
        the_file.close()
        return count


def train():
    corpus = MyCodeCorpus()
    tfidf = models.TfidfModel(corpus)
    tfidf.save('code_tfidf_for_LDA.model')
    corpus_tfidf = tfidf[corpus]
    lda = models.LdaModel(corpus, id2word=dictionary, num_topics=number, iterations=8000)
    lda.save('code_trained_LDA_model.model')
    topics = lda.print_topics(num_topics=20, num_words=30)
    pprint(topics)
    index = similarities.MatrixSimilarity(lda[corpus])
    tf_idf_index = similarities.MatrixSimilarity(corpus_tfidf, num_features=len(dictionary.keys()))
    index.save('code_trained_LDA_index.index')
    tf_idf_index.save('code_trained_tfidf_for_LDA_index.index')
    print('trained!')


train()
