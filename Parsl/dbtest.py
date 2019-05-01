## dbtest.py - test accessing a sqlite3 database via python

## The idea is not to replace the "sqlite3" interactive command, but
## to create some useful summaries specific to Parsl workflows.

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
    result = cur.execute(sql)
    rows = result.fetchall()   # <-- This is a list of db rows in the result set
    ## This will generate a list of column headings (titles) for the result set
    titles = result.description
    return (rows,titles)

def printRow(titles,row):
    ## Pretty print one row with associated column names
    for row in rows:
        print ("row ",row,":")
        for title,col in zip(titles,row):
            print(title[0],": ",col)
            pass
        break
        pass

## Connect to sqlite3 database file & create a 'cursor'
con = sqlite3.connect('monitoring.db')
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


## Print out an annotated single row from the table
row = rows[0]
printRow(titles,row)
    




sys.exit()

