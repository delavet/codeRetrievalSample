def file_len(file_name):
    count = 0
    the_file = open(file_name, encoding='utf-8')
    while True:
        buffer = the_file.read(1024 * 8192)
        if not buffer:
            break
        count += buffer.count('\n')
    the_file.close()
    return count