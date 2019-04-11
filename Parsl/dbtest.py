## dbtest.py - test accessing a sqlite3 database via python


import sys,os
import sqlite3

def getTableList(cursor):
    ##
    ## Fetch list of all tables in this database
    ##
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rawTableList = cur.fetchall()
    tableList = []
    for table in rawTableList:
        tableList.append(table[0])
        pass
    return tableList


def getTableSchema(cur,table='all'):
    ##
    ## Fetch the schema for a table
    ##
    if table == 'all':
        ### Get schema for all tables
        sql = "select sql from sqlite_master where type = 'table' ;"
    else:
        ### Get schema for a specific table
        sql = "select sql from sqlite_master where type = 'table' and name = '"+table+"';"
    cur.execute(sql)
    schemas = cur.fetchall()
    return schemas

def stdQuery(cur,sql):
    ##
    ## Perform a query, fetch all results and column headers
    result = cur.execute(q)
    rows = result.fetchall()   # <-- This is a list of db rows in the result set
    ## This will generate a list of column headings (titles) for the result set
    titles = result.description
    return (rows,titles)


## Connect to sqlite3 database file
con = sqlite3.connect('mon.db')

## Create a "cursor" for the database
cur = con.cursor()

## Fetch a list of all tables in this database
tableList = getTableList(cur)
print(tableList)

## Print out a single table schema
table = tableList[0]
schemas = getTableSchema(cur,table)
#print("schemas = ",schemas[0][0])


## Construct and perform a query
q = "select * from task"
(rows,titles) = stdQuery(cur,q)
print("#rows in result set = ",len(rows))


## Print out an annotated dump of the result set
for row in rows:
    print ("row ",row,":")
    for title,col in zip(titles,row):
        print(title[0],": ",col)
        pass
    break
    pass
    




sys.exit()

task = cur.fetchall()

print("type(task) = ",type(task))
print("len(task) = ",len(task))

