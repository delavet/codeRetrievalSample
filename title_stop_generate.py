from collections import defaultdict
import heapq
all_cnt = 16986
elect = 200
unigram_file = open('title_unigram_stops', 'w', encoding='utf-8')
preprocessed_file = open('title_mid_preprocessed1', 'r', encoding='utf-8')
frequency = defaultdict(int)
for line in preprocessed_file:
    unigrams = line.strip('\n').split(',')
    for token in unigrams:
        frequency[token] += 1
top50 = heapq.nlargest(elect, frequency.values())
print(top50)
for key in frequency.keys():
    if frequency[key] in top50:
        unigram_file.write(key+":"+str(frequency[key])+'\n')
unigram_file.close()
preprocessed_file.close()

preprocessed_file = open('title_mid_preprocessed1', 'r', encoding='utf-8')
bigram_file = open('title_bigram_stops', 'w', encoding='utf-8')
bifrequency = defaultdict(int)
for line in preprocessed_file:
    tokens = line.strip('\n').split(',')
    bigrams = []
    for i in range(len(tokens)):
        if i >= len(tokens) - 1:
            break
        bigrams.append(tokens[i]+' '+tokens[i+1])
    for bigram in bigrams:
        bifrequency[bigram] += 1
bitop50 = heapq.nlargest(elect, bifrequency.values())
print(bitop50)
for key in bifrequency.keys():
    if bifrequency[key] in bitop50:
        bigram_file.write(key+":"+str(bifrequency[key])+'\n')
bigram_file.close()
preprocessed_file.close()

preprocessed_file = open('title_mid_preprocessed1', 'r', encoding='utf-8')
trigram_file = open('title_trigram_stops', 'w', encoding='utf-8')
trifrequency = defaultdict(int)
for line in preprocessed_file:
    tokens = line.strip('\n').split(',')
    trigrams = []
    for i in range(len(tokens)):
        if i >= len(tokens) - 2:
            break
        trigrams.append(tokens[i]+' '+tokens[i+1]+' '+tokens[i+2])
    for trigram in trigrams:
        trifrequency[trigram] += 1
tritop50 = heapq.nlargest(elect, trifrequency.values())
print(tritop50)
for key in trifrequency.keys():
    if trifrequency[key] in tritop50:
        trigram_file.write(key+":"+str(trifrequency[key])+'\n')
trigram_file.close()
preprocessed_file.close()
