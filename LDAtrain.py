import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models, similarities
from pprint import pprint

preprocessed_file = open('preprocessed', 'r', encoding='utf-8')
texts = [line.strip('\n').split(',') for line in preprocessed_file]
dictionary = corpora.Dictionary(texts)

number = 140


class MyCorpus(object):
    def __iter__(self):
        for line in open('preprocessed', encoding='utf-8'):
            yield dictionary.doc2bow(line.strip('\n').split(','))

    def __len__(self):
        count = 0
        the_file = open('preprocessed', encoding='utf-8')
        while True:
            buffer = the_file.read(1024 * 8192)
            if not buffer:
                break
            count += buffer.count('\n')
        the_file.close()
        return count


def train():
    corpus = MyCorpus()
    tfidf = models.TfidfModel(corpus)
    tfidf.save('tfidf_for_LDA.model')
    corpus_tfidf = tfidf[corpus]
    lda = models.LdaModel(corpus, id2word=dictionary, num_topics=number, iterations=8000)
    lda.save('trained_LDA_model.model')
    index = similarities.MatrixSimilarity(lda[corpus_tfidf])
    index.save('trained_LDA_index.index')
    print('trained!')


train()

