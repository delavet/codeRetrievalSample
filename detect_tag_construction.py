import psycopg2
from collections import defaultdict
import sys
from pprint import pprint
tag_frequency = defaultdict(int)
conn = psycopg2.connect(database="stackoverflow", user="dell", password="dell", host="162.105.88.50", port="5432")
cur = conn.cursor()
tag_construction_file = open('tag_construction', 'w', encoding='utf-8')
sys.stdout = tag_construction_file


def get_tags():
    cur.execute("SELECT \"Tags\" FROM posts WHERE \"PostTypeId\" = 1 AND \"Tags\" Like \'%<java>%\' LIMIT 500000")
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
            tag_frequency[tag] += 1
    pprint(sorted(tag_frequency.items(), key=lambda item: -item[1]))


get_tags()
tag_construction_file.close()
conn.commit()
cur.close()
conn.close()
