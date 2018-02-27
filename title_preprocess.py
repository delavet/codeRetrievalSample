from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from collections import defaultdict
frequency = defaultdict(int)
post_file = open('title', 'r', encoding='utf-8')
mid_file = open('mid_process', 'w', encoding='utf-8')
final_file = open('title_preprocessed', 'w', encoding='utf-8')
english_stopwords = stopwords.words('english')
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '{', '}',  '&', '!', '*', '@', '#', '$', '%', '<', '>', '...', '-', '_', '\'\'', '""', '\'', '"', '``', '`']
st = LancasterStemmer()
for post in post_file:
    result = [word.lower() for word in word_tokenize(post)]
    i = 0
    while i < len(result):
        if result[i] in english_stopwords:
            result.pop(i)
            continue
        is_soy = True
        for j in range(len(result[i])):
            if result[i][j].isalpha():
                is_soy = False
        if is_soy:
            result.pop(i)
            continue
        result[i] = st.stem(result[i])
        frequency[result[i]] += 1
        i += 1

    result_word = ','.join(result)+'\n'
    mid_file.write(result_word)
mid_file.close()
mid_file = open('mid_process', 'r', encoding='utf-8')
for line in mid_file:
    tokens = line.strip('\n').split(',')
    tokens = [token for token in tokens if frequency[token] > 1]
    result_word = ','.join(tokens)+'\n'
    final_file.write(result_word)
final_file.close()
post_file.close()
