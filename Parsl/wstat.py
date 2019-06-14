## wstat.py - workflow status summary from Parsl monitoring database

## The idea is not to replace the "sqlite3" interactive command, but
## to create some useful summaries specific to Parsl workflows.

## This version is tracking Parsl 0.8.0a

## T.Glanzman - Spring 2019
__version__ = "0.7.1"
pVersion='0.8.0a'

import sys,os
import sqlite3
from tabulate import tabulate
import datetime
import argparse

class pmon:
    ### class pmon - interpret Parsl monitoring database
    def __init__(self,dbfile='monitoring.db'):
        ## Instance variables
        self.dbfile = dbfile

        ## Prepare data 
        self.con = sqlite3.connect(self.dbfile)      ## connect to sqlite3 file
        self.con.row_factory = sqlite3.Row           ## optimize output format
        self.cur = self.con.cursor()                       ## create a 'cursor'
        self.readWorkflowTable()                          ## read the workflow table
        return


    def __del__(self):
        ## Class destructor 
        self.con.close()


    def readWorkflowTable(self,sql="select * from workflow"):
        ## Extract all rows from 'workflow' table
        ## This alternate query returns a list of one 'row' containing the most recent entry
        #sql = "select * from workflow order by time_began desc limit 1"
        (self.wrows,self.wtitles) = self.stdQuery(sql)
        return


    def getTableList(self):
        ## Fetch list of all tables in this database
        ## Parsl monitoring.db currently contains four tables: resource, status, task, workflow
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        rawTableList = self.cur.fetchall()
        tableList = []
        for table in rawTableList:
            tableList.append(table[0])
            pass
        return tableList


    def getTableSchema(self,table='all'):
        ## Fetch the schema for one or more tables
        if table == 'all':
            sql = "select sql from sqlite_master where type = 'table' ;"
        else:
            sql = "select sql from sqlite_master where type = 'table' and name = '"+table+"';"
        self.cur.execute(sql)
        schemas = self.cur.fetchall()
        return schemas


    def printRow(self,titles,row):
        ## Pretty print one row with associated column names
        for title,col in zip(titles,row):
            print(title[0],": ",col)
            pass
        pass
        return


    def stdQuery(self,sql):
        ## Perform a query, fetch all results and column headers
        result = self.cur.execute(sql)
        rows = result.fetchall()   # <-- This is a list of db rows in the result set
        ## This will generate a list of column headings (titles) for the result set
        titlez = result.description
        ## Convert silly 7-tuple title into a single useful value
        titles = []
        for title in titlez:
            titles.append(title[0])
            pass
        return (rows,titles)


    def printWorkflowSummary(self):
        ## Summarize current state of workflow
        ## workflow table:  ['run_id', 'workflow_name', 'workflow_version', 'time_began', 
        ##                           'time_completed', 'workflow_duration', 'host', 'user', 'rundir', 
        ##                           'tasks_failed_count', 'tasks_completed_count']
        repDate = datetime.datetime.now()
        rows = self.wrows
        titles = self.wtitles

        nRuns = len(rows)
        row = rows[-1]                    # Grab the last row in the workflow table == most recent run

        runNum = os.path.basename(row['rundir'])
        irunNum = int(runNum)
        runID = row['run_id']
        exeDir = os.path.dirname(os.path.dirname(row['rundir']))

        completedTasks = row['tasks_completed_count']+row['tasks_failed_count']

        ##   Print SUMMARIES
        print('Workflow summary\n================\n')
        wSummaryList = []
        wSummaryList.append(['Report Date/Time ',repDate ])
        wSummaryList.append(['user', row['user']])
        wSummaryList.append(['MonitorDB',self.dbfile])
        wSummaryList.append(['workflow script',os.path.join(exeDir,row['workflow_name'])])
        wSummaryList.append(['workflow node', row['host']])
        wSummaryList.append(['most recent run',runNum ])
        wSummaryList.append(['most recent run start',row['time_began'] ])
        wSummaryList.append(['most recent run end ',row['time_completed'] ])
        wSummaryList.append(['most recent run duration ', str(row['workflow_duration'])+' s'])
        wSummaryList.append(['tasks completed',completedTasks ])
        wSummaryList.append(['tasks completed: success', row['tasks_completed_count']])
        wSummaryList.append(['tasks completed: failed',row['tasks_failed_count'] ])
        print(tabulate(wSummaryList, tablefmt="grid"))
        return


    def printTaskSummary(self):
        ## The task summary is a composite of values from the 'task' and 'status' tables
        print('\n\nTask summary (*most recent run*)\n================================\n')

        ## Extract data from 'task' table
        row = self.wrows[-1]
        runID = row['run_id']
        sql = 'select task_id,hostname,task_time_submitted,task_time_running,task_time_returned,task_stdout  from task where run_id = "'+row['run_id']+'"'
        (tRowz,tTitles) = self.stdQuery(sql)

        ## Convert from sqlite3.Row to a simple 'list'
        tRows = []
        for row in tRowz:
            tRows.append(list(row))
            pass

        numTasks = len(tRows)
        print('number of Tasks dispatched = ',numTasks)

        ## Extract data from 'status' table
        tTitles.insert(1, "status")
        for row in range(numTasks):
            taskID = tRows[row][0]
            sql = 'select task_id,timestamp,task_status_name from status where run_id="'+str(runID)+'" and task_id="'+str(taskID)+'" order by timestamp desc limit 1'
            (sRowz,sTitles) = self.stdQuery(sql)
            tRows[row].insert(1, sRowz[0]['task_status_name'])
            pass

        ## Pretty print task summary table
        print(tabulate(tRows,headers=tTitles,tablefmt="grid"))
        return


    def standardSummary(self):
        ## This is the standard summary: workflow summary + summary of tasks in current run
        self.printWorkflowSummary()
        self.printTaskSummary()
        return

    def shortSummary(self):
        ## This is the short summary:
        self.printWorkflowSummary()
        return

    def workflowHistory(self):
        ## This is the workflowHistory: details for each workflow 'run'
        sql = 'select workflow_name,user,host,time_began,time_completed,tasks_completed_count,tasks_failed_count,rundir from workflow'
        (wrows,wtitles) = self.stdQuery(sql)
        ## Modify the result set
        for i in list(range(len(wtitles))):
            if wtitles[i] == 'tasks_completed_count':wtitles[i] = '#tasks_good'
            if wtitles[i] == 'tasks_failed_count':wtitles[i] = '#tasks_bad'
            pass
        rows = []
        wtitles.insert(0,"RunNum")
        for wrow in wrows:
            row = list(wrow)
            if row[4] is None: row[4] = '-> running or killed <-'
            row.insert(0,os.path.basename(row[7]))
            rows.append(row)
        ## Print the report
        print(tabulate(rows,headers=wtitles, tablefmt="psql"))
        return


####################################################
##
##                                   M A I N
##
####################################################


if __name__ == '__main__':


    reportTypes = ['standardSummary','shortSummary','workflowHistory']

    ## Parse command line arguments
    parser = argparse.ArgumentParser(description='A simple Parsl status reporter.  Available reports include:'+str(reportTypes))
    parser.add_argument('reportType',help='Type of report to display (default=%(default)s)',nargs='?',default='standardSummary')
    parser.add_argument('-f','--file',default='monitoring.db',help='name of Parsl monitoring database file (default=%(default)s)')
    parser.add_argument('-s','--schemas',action='store_true',default=False,help="only print out monitoring db schema for all tables")
    parser.add_argument('-v','--version', action='version', version=__version__)
    args = parser.parse_args()

    print('\nwstat (version ',__version__,', written for Parsl version '+pVersion+')\n')

    ## Create a Parsl Monitor object
    m = pmon()

    ## Print out table schemas only
    if args.schemas:
        ## Fetch a list of all tables in this database
        tableList = m.getTableList()
        print('Tables: ',tableList)

        ## Print out schema for all tables
        for table in tableList:
            schema = m.getTableSchema(table)
            print(schema[0][0])
            pass
        sys.exit()

    ## Print out requested report
    if args.reportType not in reportTypes: sys.exit(1)
    if args.reportType == 'standardSummary':
        m.standardSummary()
    if args.reportType == 'shortSummary':
        m.shortSummary()
    if args.reportType == 'workflowHistory':
        m.workflowHistory()
 
    ## Done
    sys.exit()

