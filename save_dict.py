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