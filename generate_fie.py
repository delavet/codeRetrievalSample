import psycopg2
from bs4 import BeautifulSoup
conn = psycopg2.connect(database="stackoverflow", user="dell", password="dell", host="162.105.88.50", port="5432")
cur = conn.cursor()
answer_cur = conn.cursor()
body_file = open('body', 'w', encoding='utf-8')
post_file = open('post', 'w', encoding='utf-8')
code_file = open('code', 'w', encoding='utf-8')
title_file = open('title', 'w', encoding='utf-8')
id_file = open('id', 'w', encoding='utf-8')
topic_file = open('topics', 'r', encoding='utf-8')

question_found = 0
topics = topic_file.readlines()
i = 0
for a in topics:
    topics[i] = a.strip('\n')
    i += 1


def get_by_tags():
    global question_found
    print(topics)
    cur.execute("SELECT \"Id\",\"Body\",\"Tags\",\"Title\" FROM posts WHERE \"PostTypeId\" = 1 LIMIT 1000000")

    while 1:
        row = cur.fetchone()
        if row == None:
            break
        if row[2] == None:
            continue
        tags = str(row[2]).strip('<').strip('>').split("><")
        # if 'java' not in tags:
        #    continue
        haveTag = False
        for tag in tags:
            if tag in topics:
                haveTag = True
        if haveTag == False:
            continue

        question_found += 1

        answer_query = "SELECT \"Body\" FROM posts WHERE \"ParentId\" = " + str(row[0])
        answer_cur.execute(answer_query)
        answers = answer_cur.fetchall()

        temp_body = row[1]
        for answer in answers:
            temp_body = temp_body + answer[0]
        soup = BeautifulSoup(temp_body, "html.parser")
        temp_code = ''
        for code in soup.find_all('pre'):
            temp_code = temp_code + code.get_text() + '\t'
            code.clear()
        temp_code.strip('\t')
        id_file.write(str(row[0]) + '\n')
        body_file.write(str((temp_body.replace('\r\n', ' ').replace('\n', ' ')))+'\n')
        post_file.write(str((soup.get_text().replace('\r\n', ' ').replace('\n', ' ')))+'\n')
        code_file.write(str((temp_code.expandtabs(1).replace('\r\n', '\t').replace('\n', '\t')))+'\n')
        title_file.write(str((row[3].replace('\r\n', ' ').replace('\n', ' ')))+'\n')


get_by_tags()
print(question_found)

topic_file.close()
code_file.close()
post_file.close()
body_file.close()
conn.commit()
cur.close()
answer_cur.close()
conn.close()
'''
.encode("utf-8", "surrogateescape")
'''