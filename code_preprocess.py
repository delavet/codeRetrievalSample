from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import defaultdict
frequency = defaultdict(int)
code_file = open('code', 'r', encoding='utf-8')
mid_file = open('code_mid_process', 'w', encoding='utf-8')
final_file = open('code_mid_preprocessed1', 'w', encoding='utf-8')
none_full_alpha_record = open('code_none_full_alpha_record', 'w', encoding='utf-8')
splitters = ['-', '_']
st = PorterStemmer()
for code in code_file:
    tokens = list(word_tokenize(code))
    result = []
    i = 0 
    buffer_str = ''
    while i < len(result):
        for j in range(len(tokens[i])):
            if tokens[i][j].isalpha() and tokens[i][j] >= 'A' and tokens[i][j] <='Z' and buffer_str != '':
                result.append(buffer_str.lower())
                buffer_str = tokens[i][j]
            elif tokens[i][j] in splitters and buffer_str != '':
                result.append(buffer_str.lower())
            else:
                 buffer_str += tokens[i][j]
        i += 1
    i = 0
    while i < len(result):
        is_soy = True
        full_alpha = True
        for j in range(len(result[i])):
            if result[i][j].isalpha():
                is_soy = False
            if not result[i][j].isalpha():
                full_alpha = False
        if is_soy:
            result.pop(i)
            continue
        if not full_alpha:
            none_full_alpha_record.write(result[i]+'\n')
        result[i] = st.stem(result[i])
        frequency[result[i]] += 1
        i += 1
        
    result_word = ','.join(result)+'\n'
    mid_file.write(result_word)
    
mid_file.close()
mid_file = open('code_mid_process', 'r', encoding='utf-8')
for line in mid_file:
    tokens = line.strip('\n').split(',')
    tokens = [token for token in tokens if frequency[token] > 3]
    result_word = ','.join(tokens)+'\n'
    final_file.write(result_word)
final_file.close()
code_file.close()
print('done')

'''
lines = post_file.readlines()
post_lines = [line.split('\t', 1)[1] for line in lines]
print('a')
post_tokenized = [[word.lower() for word in word_tokenize(document)] for document in post_lines]
english_stopwords = stopwords.words('english')
print('b')
post_filtered_stop = [[word for word in document if word not in english_stopwords] for document in post_tokenized]
print('c')
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
post_filtered = [[word for word in document if word not in english_punctuations] for document in post_filtered_stop]
st = LancasterStemmer()
print('d')
post_stemmed = [[st.stem(word) for word in document] for document in post_filtered]
print('e')
#all_stems = []
#i = 0
#for stems in post_stemmed:
#   all_stems.extend(stems)
#   i = i + 1
#    print(i)
#stems_once = [stem for stem in all_stems if all_stems.count(stem) == 1]
#print('f')
#final = [[stem for stem in text if stem not in stems_once] for text in post_stemmed]
print('g')
final_file = open('preprocessed', 'w', encoding='utf-8')
final_lines = [','.join(final_line)+'\n' for final_line in post_stemmed]
print('h')
final_file.writelines(final_lines)
final_file.close()
post_file.close()
'''
