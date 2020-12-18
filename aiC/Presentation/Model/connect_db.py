import sqlite3
import pandas as pd

def getfile():
    mydb=sqlite3.connect(r'C:\Users\75085\Desktop\Presentation\Model\db.sqlite3')
    cursor=mydb.cursor()

    cursor.execute('SELECT * FROM Colleges;')
    Colleges=pd.DataFrame(cursor.fetchall())
    Colleges.drop(labels=[2,3,4,5],axis=1,inplace=True)
    Colleges=Colleges.groupby(0)[1].apply(list).to_dict()

    cursor.execute('SELECT * FROM Category;')
    Category=pd.DataFrame(cursor.fetchall())
    Category=Category.groupby(0)[1].apply(list).to_dict()

    cursor.execute('SELECT * FROM Provinces;')
    Provinces=pd.DataFrame(cursor.fetchall())
    Provinces=Provinces.groupby(0)[1].apply(list).to_dict()

    cursor.execute('SELECT collegeName,Majors.year,provinceNAME,categoryname,majorName,minScore,rank FROM Majors,Provinces,Colleges,Category,Rankings where Majors.provinceID_id=Provinces.provinceID and Majors.collegeID_id=Colleges.collegeID and Majors.categoryID_id=Category.categoryID and Rankings.year=Majors.year and Rankings.score=Majors.minScore and Rankings.categoryID_id=Majors.categoryID_id and Rankings.provinceID_id=Majors.provinceID_id;')
    rank=pd.DataFrame(cursor.fetchall())
    #print(rank.head(10),rank.shape)


    rank.rename(columns={0:'College',1:'Year',2:'Province',3:'category',4:'Major',5:'score',6:'rank'},inplace=True)
    rank['Contributor']=''
    rank.to_csv("Model/rank.csv",index=False)
    print(rank.head())

getfile()