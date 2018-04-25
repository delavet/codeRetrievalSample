from gensim import corpora
# must save dict before import this py file, use save_dict.py
t_dictionary = corpora.Dictionary.load("t_dict.dict")
p_dictionary = corpora.Dictionary.load("p_dict.dict")
c_dictionary = corpora.Dictionary.load("c_dict.dict")


class MyTitleCorpus(object):
    def __iter__(self):
        for line in open('title_preprocessed', encoding='utf-8'):
            yield t_dictionary.doc2bow(line.strip('\n').split(','))

    def __len__(self):
        count = 0
        the_file = open('title_preprocessed', encoding='utf-8')
        while True:
            buffer = the_file.read(1024 * 8192)
            if not buffer:
                break
            count += buffer.count('\n')
        the_file.close()
        return count


class MyCorpus(object):
    def __iter__(self):
        for line in open('preprocessed', encoding='utf-8'):
            yield p_dictionary.doc2bow(line.strip('\n').split(','))

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


class MyCodeCorpus(object):
    def __iter__(self):
        for line in open('code_preprocessed', encoding='utf-8'):
            yield c_dictionary.doc2bow(line.strip('\n').split(','))

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
