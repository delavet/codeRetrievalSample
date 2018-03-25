import psycopg2
conn = psycopg2.connect(database="stackoverflow", user="dell", password="dell", host="162.105.88.50", port="5432")
cur = conn.cursor()
answer_cur = conn.cursor()
tag_file = open('java_tags_record', 'w', encoding='utf-8')
raw_tag_file = open('raw_java_tags_record', 'w', encoding='utf-8')


def get_tags():
    full_tags = []
    cur.execute("SELECT \"Tags\" FROM posts WHERE \"PostTypeId\" = 1 AND \"Tags\" Like \'%<java>%\'")
    while 1:
        row = cur.fetchone()
        if row is None:
            break
        if row[0] is None:
            continue
        tags = str(row[0]).strip('<').strip('>').split("><")
        if 'java' not in tags:
            continue
        for tag in tags:
            if tag not in full_tags:
                full_tags.append(tag+'\n')
        raw_tag_file.write(row[0] + '\n')
    tag_file.writelines(full_tags)


get_tags()
raw_tag_file.close()
tag_file.close()
conn.commit()
cur.close()
conn.close()
