import psycopg2
conn = psycopg2.connect(database="stackoverflow", user="dell", password="dell", host="162.105.88.50", port="5432")
cur = conn.cursor()
topic_file = open('topics', 'w', encoding='utf-8')
cur.execute("SELECT \"Id\",\"Body\",\"Tags\" FROM posts WHERE \"PostTypeId\" = 1 LIMIT 10000")

topics = []
question_found = 0
while 1:
    row = cur.fetchone()
    if row == None:
        break
    if row[2] == None:
        continue

    tags = str(row[2]).strip('<').strip('>').split("><")
    cont = False
    for t in tags:
        if t in topics:
            cont = True
    if cont:
        continue
    topics.extend([t for t in tags if t not in topics])
    if len(topics) > 50:
        break

print(len(topics))
for topic in topics:
    topic_file.write(topic+'\n')
topic_file.close()
conn.commit()
cur.close()
conn.close()
