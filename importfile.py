from app import *
import csv
with open ('yzp_blog_1.csv') as file:
    Generaldata = csv.reader(file)
    i=0
    for row in Generaldata:
        squ1=BlogingPost(title=row[3],content=row[1],datime=row[2])
        db.session.add(squ1)
        db.session.commit()
