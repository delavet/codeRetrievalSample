preprocessed = open('preprocessed', 'r', encoding='utf-8')
detected_file = open('none_alpha_detected_after_preprocess', 'w', encoding='utf-8')
for line in preprocessed:
    tokens = line.strip('\n').split(',')
    for token in tokens:
        detected = False
        for i in range(len(token)):
            if not token[i].isalpha():
                detected = True
                break
        if detected:
            write_word = token + '\n'
            detected_file.write(write_word)
detected_file.close()
preprocessed.close()
