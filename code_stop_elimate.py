unigram_file = open('code_unigram_stops', 'r', encoding='utf-8')
bigram_file = open('code_bigram_stops', 'r', encoding='utf-8')
trigram_file = open('code_trigram_stops', 'r', encoding='utf-8')
preprocessed_file = open('code_mid_preprocessed1', 'r', encoding='utf-8')
final_file = open('code_preprocessed', 'w', encoding='utf-8')

unigrams = unigram_file.readlines()
bigrams = bigram_file.readlines()
trigrams = trigram_file.readlines()
for i in range(len(unigrams)):
    unigrams[i] = unigrams[i].strip('\n')
for i in range(len(bigrams)):
    bigrams[i] = bigrams[i].strip('\n')
for i in range(len(trigrams)):
    trigrams[i] = trigrams[i].strip('\n')
for line in preprocessed_file:
    tokens = line.strip('\n').split(',')
    i = 0
    while i < len(tokens) - 2:
        tri = tokens[i] + ' ' + tokens[i + 1] + ' ' + tokens[i + 2]
        found = False
        for t in trigrams:
            if tri == t:
                tokens.pop(i)
                tokens.pop(i)
                tokens.pop(i)
                found = True
        if not found:
            i += 1
    i = 0
    while i < len(tokens) - 1:
        bi = tokens[i] + ' ' + tokens[i + 1]
        found = False
        for b in bigrams:
            if bi == b:
                tokens.pop(i)
                tokens.pop(i)
                found = True
        if not found:
            i += 1
    i = 0
    while i < len(tokens):
        uni = tokens[i]
        found = False
        for u in unigrams:
            if uni == u:
                tokens.pop(i)
                found = True
        if not found:
            i += 1
    result = ','.join(tokens)+'\n'
    final_file.write(result)

final_file.close()
preprocessed_file.close()
trigram_file.close()
bigram_file.close()
unigram_file.close()