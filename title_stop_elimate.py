unigram_file = open('title_unigram_stops', 'r', encoding='utf-8')
bigram_file = open('title_bigram_stops', 'r', encoding='utf-8')
trigram_file = open('title_trigram_stops', 'r', encoding='utf-8')
preprocessed_file = open('title_mid_preprocessed1', 'r', encoding='utf-8')
final_file = open('title_preprocessed', 'w', encoding='utf-8')

unigrams = unigram_file.readlines()
bigrams = bigram_file.readlines()
trigrams = trigram_file.readlines()
for i in range(len(unigrams)):
    unigrams[i] = unigrams[i].strip('\n')
for line in preprocessed_file:
    tokens = line.strip('\n').split(',')
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
