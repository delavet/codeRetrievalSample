from gensim import corpora

t_preprocessed_file = open('title_preprocessed', 'r', encoding='utf-8')
t_dictionary = corpora.Dictionary(line.strip('\n').split(',') for line in t_preprocessed_file)
t_preprocessed_file.close()

p_preprocessed_file = open('preprocessed', 'r', encoding='utf-8')
p_dictionary = corpora.Dictionary(line.strip('\n').split(',') for line in p_preprocessed_file)
p_preprocessed_file.close()

c_preprocessed_file = open('code_preprocessed', 'r', encoding='utf-8')
c_dictionary = corpora.Dictionary(line.strip('\n').split(',') for line in c_preprocessed_file)
c_preprocessed_file.close()

t_dictionary.save("t_dict.dict")
p_dictionary.save("p_dict.dict")
c_dictionary.save("c_dict.dict")


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