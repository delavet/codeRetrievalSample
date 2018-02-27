import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models, similarities
from pprint import pprint

preprocessed_file = open('preprocessed', 'r', encoding='utf-8')
texts = [line.strip('\n').split(',') for line in preprocessed_file]
dictionary = corpora.Dictionary(texts)
pprint(dictionary.token2id)

number = 10


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


corpus = MyCorpus()
tfidf = models.TfidfModel(corpus)
tfidf.save('tfidf_for_LDA.model')
corpus_tfidf = tfidf[corpus]
#while number < 410:
#    lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=number)
#    lda.save('trained_model'+str(number)+'.model')
#    index = similarities.MatrixSimilarity(lda[corpus])
#    index.save('trained_index'+str(number)+'.index')
#    number += 10
#hdp = models.HdpModel(corpus, id2word=dictionary)
#hdp.save('trainedHdp.model')
#lda = hdp.suggested_lda_model()
#lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=number)
lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics= 20)
lda.save('trained_LDA_model.model')
index = similarities.MatrixSimilarity(lda[corpus_tfidf])
index.save('trained_LDA_index.index')

print('trained!')

3540
