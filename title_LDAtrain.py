import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models, similarities

preprocessed_file = open('title_preprocessed', 'r', encoding='utf-8')
dictionary = corpora.Dictionary(line.strip('\n').split(',') for line in preprocessed_file)

number = 10


class MyCorpus(object):
    def __iter__(self):
        for line in open('final', encoding='utf-8'):
            yield dictionary.doc2bow(line.strip('\n').split(','))

    def __len__(self):
        count = 0
        the_file = open('final', encoding='utf-8')
        while True:
            buffer = the_file.read(1024 * 8192)
            if not buffer:
                break
            count += buffer.count('\n')
        the_file.close()
        return count


corpus = MyCorpus()
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
#while number < 410:
#    lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=number)
#    lda.save('trained_model'+str(number)+'.model')
#    index = similarities.MatrixSimilarity(lda[corpus])
#    index.save('trained_index'+str(number)+'.index')
#    number += 10
#hdp = models.HdpModel(corpus_tfidf, id2word=dictionary)
#hdp.save('trainedHdp.model')
#lda = hdp.suggested_lda_model()
lda = models.LdaModel(corpus, id2word=dictionary, num_topics=number)
topic_num = lda.get_topics().size
print(topic_num)
lda.save('ttrained_model.model')
index = similarities.MatrixSimilarity(lda[corpus])
index.save('ttrained_index.index')

print('trained!')

3540
