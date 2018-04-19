def trans_stop(file_name):
    file = open(file_name, 'r', encoding='utf-8')
    stop_lines = file.readlines()
    file.close()
    wfile = open(file_name, 'w', encoding='utf-8')
    for line in stop_lines:
        stop = (line.split(':'))[0]
        wfile.write(stop+"\n")


trans_stop('unigram_stops')
trans_stop('bigram_stops')
trans_stop('trigram_stops')
trans_stop('code_unigram_stops')
trans_stop('code_bigram_stops')
trans_stop('code_trigram_stops')
trans_stop('title_unigram_stops')
trans_stop('title_bigram_stops')
trans_stop('title_trigram_stops')
print('done')
