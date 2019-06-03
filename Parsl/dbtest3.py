## dbtest.py - test accessing a sqlite3 database via python

## The idea is not to replace the "sqlite3" interactive command, but
## to create some useful summaries specific to Parsl workflows.

## This version is tracking Parsl 0.8.0a (informal designation)

## T.Glanzman - Spring 2019

import sys,os
import sqlite3
from tabulate import tabulate
import datetime

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
    titlez = result.description

    ## Convert silly 7-tuple title into a single useful value
    titles = []
    for title in titlez:
        titles.append(title[0])
        pass
    return (rows,titles)


def printRow(titles,row):
    ## Pretty print one row with associated column names
    #print('type(row) = ',type(row))
    #print('row = ',row)
    #print('titles = ',titles)
    for title,col in zip(titles,row):
        print(title[0],": ",col)
        pass
    pass

####################################################
####################################################


## Parsl monitoring.db contains four tables: resource, status, task, workflow

## Connect to sqlite3 database file & create a 'cursor'

con = sqlite3.connect('monitoring.db')
print('con.row_factory = ',con.row_factory)

con.row_factory = sqlite3.Row
cur = con.cursor()


## Fetch a list of all tables in this database
tableList = getTableList(cur)
#print(tableList)
print('Tables: ',tableList)


## Print out a single table schema
table = tableList[0]
schemas = getTableSchema(cur,table)
#print("schemas = ",schemas[0][0])



## Summarize workflow

## workflow table:  ['run_id', 'workflow_name', 'workflow_version', 'time_began', 'time_completed', 'workflow_duration', 'host', 'user', 'rundir', 'tasks_failed_count', 'tasks_completed_count']

repDate = datetime.datetime.now()

## Extract all rows from 'workflow' table
sql = "select * from workflow"
## This alternate query returns a list of one 'row' containing the most recent entry
#sql = "select * from workflow order by time_began desc limit 1"
(rows,titles) = stdQuery(cur,sql)

nRuns = len(rows)
row = rows[-1]                    # Grab the last row in the workflow table == most recent run

## Dump one row of result set using special "sqlite3.Row" feature
#print('\n\n')
#for title,item in zip(row.keys(),row):
# print(title,":   ",item)
# pass

runNum = os.path.basename(row['rundir'])
irunNum = int(runNum)
runID = row['run_id']
exeDir = os.path.dirname(os.path.dirname(row['rundir']))

totalTasks = row['tasks_completed_count']+row['tasks_failed_count']



###
###   SUMMARIES
###


print('\n\nWorkflow summary\n================\n')

wSummaryList = []
wSummaryList.append(['Report Date/Time ',repDate ])
wSummaryList.append(['user', row['user']])
wSummaryList.append(['workflow script',os.path.join(exeDir,row['workflow_name'])])
wSummaryList.append(['workflow node', row['host']])
wSummaryList.append(['most recent run',runNum ])
wSummaryList.append(['most recent run start',row['time_began'] ])
wSummaryList.append(['most recent run end ',row['time_completed'] ])
wSummaryList.append(['most recent run duration ', str(row['workflow_duration'])+' s'])
wSummaryList.append(['total tasks',totalTasks ])
wSummaryList.append(['number of successful tasks', row['tasks_completed_count']])
wSummaryList.append(['number of failed tasks',row['tasks_failed_count'] ])
#wSummaryList.append([' ', ])
#wSummaryList.append([' ', ])
print(tabulate(wSummaryList, tablefmt="grid"))


## Print entire workflow table
#print("list(row) = \n",dict(row))
#print(tabulate(list(rows),headers=titles, tablefmt="psql"))



print('\n\nTask summary (most recent run)\n==============================\n')

## The task summary is a composite of values from the 'task' and 'status' tables

## Extract data from 'task' table
sql = 'select task_id,hostname,task_time_submitted,task_time_running,task_time_returned,task_stdout  from task where run_id = "'+row['run_id']+'"'
(tRowz,tTitles) = stdQuery(cur,sql)


## Convert from sqlite3.Row to a simple 'list'
tRows = []
for row in tRowz:
    tRows.append(list(row))
    pass

numTasks = len(tRows)
print('number of Tasks dispatched = ',numTasks)

# ################# MOCK up 'node' names until it is available in the monitoring.db file
# tTitles.append("node")
# for row in range(numTasks):
#     tRows[row].append("nid00050"+str(row))
#     pass


## Extract data from 'status' table

tTitles.insert(1, "status")
for row in range(numTasks):
    taskID = tRows[row][0]
    sql = 'select task_id,timestamp,task_status_name from status where run_id="'+str(runID)+'" and task_id="'+str(taskID)+'" order by timestamp desc limit 1'
    (sRowz,sTitles) = stdQuery(cur,sql)
    tRows[row].insert(1, sRowz[0]['task_status_name'])
    pass

## Pretty print task summary table
print(tabulate(tRows,headers=tTitles,tablefmt="grid"))


###########

## Finish up and exit
con.close()
sys.exit()

