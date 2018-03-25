from nltk.stem.porter import PorterStemmer
from collections import defaultdict
import re
frequency = defaultdict(int)
code_file = open('code', 'r', encoding='utf-8')
mid_file = open('code_mid_process', 'w', encoding='utf-8')
final_file = open('code_mid_preprocessed1', 'w', encoding='utf-8')
none_full_alpha_record = open('code_none_full_alpha_record', 'w', encoding='utf-8')
splitters = ['-', '_']
st = PorterStemmer()
for code in code_file:
    code_after_first_preprocess = re.sub("[^a-zA-Z]", ",", code)
    tokens = [token for token in code_after_first_preprocess.split(",") if len(token) > 2]
    result = []
    i = 0
    buffer_str = ''
    while i < len(tokens):
        for j in range(len(tokens[i])):
            if j == 0:
                buffer_str = buffer_str + tokens[i][j]
                continue
            if tokens[i][j].isalpha() and tokens[i][j] >= 'A' and tokens[i][j] <= 'Z' and tokens[i][j-1].isalpha() and tokens[i][j-1] >= 'a' and tokens[i][j-1] <= 'z' and buffer_str != '':
                result.append(buffer_str.lower())
                buffer_str = tokens[i][j]
            else:
                buffer_str = buffer_str + tokens[i][j]
        result.append(buffer_str.lower())
        buffer_str = ''
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
        i = i + 1
    result_word = ','.join(result)+'\n'
    mid_file.write(result_word)
mid_file.close()
mid_file = open('code_mid_process', 'r', encoding='utf-8')
for line in mid_file:
    tokens = line.strip('\n').split(',')
    tokens = [token for token in tokens if frequency[token] > 10]
    result_word = ','.join(tokens)+'\n'
    final_file.write(result_word)
final_file.close()
code_file.close()
print('done')
