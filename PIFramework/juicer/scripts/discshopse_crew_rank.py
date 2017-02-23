import MySQLdb
import json
import re

#conn = MySQLdb.connect(host="localhost", user = "root", db = "FANDANGOOBDB", charset="utf8", use_unicode=True)
conn = MySQLdb.connect(host="10.28.218.81", user="root", db="CDONSEOBDB", charset="utf8", use_unicode=True)
cur = conn.cursor()

all_sks = 'select distinct program_sk from ProgramCrew'
#all_sks = "select program_sk from ProgramCrew where rank != '' group by program_sk, rank, program_type having count(*) > 1;"
cur.execute(all_sks)
sks = cur.fetchall()
for each in sks:
    query = "select program_sk, program_type, crew_sk from ProgramCrew where program_sk = '%s'" %each[0]
    cur.execute(query)
    sk_row = cur.fetchall()

    for row in sk_row:
        sk = row[0]
        _type = row[1]
        c_sk = row[2]
        all_records = "select count(*) from ProgramCrew where program_sk = '%s' and program_type = '%s'" %(sk, _type)
        cur.execute(all_records)

        crews_sk = "select crew_sk from ProgramCrew where program_sk = '%s' and program_type = '%s'" %(sk, _type)
        cur.execute(crews_sk)
        crew_sks = cur.fetchall()
        i = 0
        for crews in  crew_sks:
            count_range = len(crew_sks)
            crew_sk = crews[0]
            i = i + 1
            try:
                query2 = "update ProgramCrew set rank = '%s' where program_sk = '%s' and program_type = '%s' and crew_sk = '%s'" %(i, sk, _type, crew_sk)
                cur.execute(query2)
            except:
                query2 = 'update ProgramCrew set rank = "%s" where program_sk = "%s" and program_type = "%s" and crew_sk = "%s"' %(i, sk, _type, crew_sk)
                cur.execute(query2)
