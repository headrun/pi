import MySQLdb as dbapi
import sys 
import csv 

class CSVGen():
   def csv_generation(self):
       dbServer='localhost'
       dbPass='root'
       dbSchema='AMAZON'
       dbUser='root'
       dbQuery='SELECT * FROM INELEMENT.Product;'
       db=dbapi.connect(host=dbServer,user=dbUser,passwd=dbPass)
       cur=db.cursor()
       cur.execute(dbQuery)
       result=cur.fetchall()
       c = csv.writer(open("/home/sumanth/GenFramework/juicer/OTT_CFW/Inelement.csv","wb"))
       for row in result:
           c.writerow(row)
       cur.close()

   def main(self):
       self.csv_generation()
obj = CSVGen()
obj.csv_generation()
