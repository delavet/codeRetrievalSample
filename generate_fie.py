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
tag_file = open('tags_record', 'w', encoding='utf-8')
tbody = open('tbody', 'w', encoding='utf-8')


question_found = 0


def get_by_tags():
    global question_found
    cur.execute("SELECT \"Id\",\"Body\",\"Tags\",\"Title\" FROM posts WHERE \"PostTypeId\" = 1 AND \"Tags\" Like \'%<java>%\' LIMIT 100000")
    while 1:
        row = cur.fetchone()
        if row is None:
            break
        if row[2] is None:
            continue
        tags = str(row[2]).strip('<').strip('>').split("><")
        if 'java' not in tags:
            continue
        tag_file.write(row[2] + '\n')
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
        try:
            id_str = str(row[0]) + '\n'
            body_str = str((temp_body.replace('\r\n', ' ').replace('\n', ' ')))+'\n'
            post_str = str((soup.get_text(separator=",").replace('\r\n', ' ').replace('\n', ' ')))+'\n'
            code_str = str((temp_code.expandtabs(1).replace('\r\n', '\t').replace('\n', '\t')))+'\n'
            title_str = str((row[3].replace('\r\n', ' ').replace('\n', ' ')))+'\n'
            id_str = id_str.encode("utf-8", "surrogateescape").decode("utf-8")
            body_str = body_str.encode("utf-8", "surrogateescape").decode("utf-8")
            post_str = post_str.encode("utf-8", "surrogateescape").decode("utf-8")
            code_str = code_str.encode("utf-8", "surrogateescape").decode("utf-8")
            title_str = title_str.encode("utf-8", "surrogateescape").decode("utf-8")
            tbody.write(post_str)
        except Exception:
            pass
        else:
            id_file.write(id_str)
            body_file.write(body_str)
            post_file.write(post_str)
            code_file.write(code_str)
            title_file.write(title_str)


get_by_tags()
print(question_found)
tbody.close()
tag_file.close()
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
