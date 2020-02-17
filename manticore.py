#!/usr/bin/env python3

import os
import sys
import time
import socket
import pymysql.cursors

hostname = os.environ['COLLECTD_HOSTNAME'] if 'COLLECTD_HOSTNAME' in os.environ else socket.getfqdn()
interval = float(os.environ['COLLECTD_INTERVAL']) if 'COLLECTD_INTERVAL' in os.environ else 1

settings = {'host': '0', 'port': 9306, 'connect_timeout': 3}
stats = {'fields': ['connections','queries','qcache_hits', 'command_search']}
types = { 'connections': 'connections' ,'queries': 'operations','qcache_hits': 'cache_operation', 'command_search': 'operations' }
'''
command_excerpt  
command_update   
command_delete   
command_keywords 
command_persist  
command_status   
command_flushattrs
command_set      
command_insert   
command_replace  
command_commit   
command_suggest  
command_json     
command_callpq   ''' 
instance=''

def printvals(values, instance='default'):
    for counter in values:
        print('PUTVAL "%s/manticore-%s/%s-%s" interval=%s N:%s' % (hostname, instance, types[counter],counter, interval, values[counter]))
        sys.stdout.flush()
    

def main():
    if len(sys.argv)<2:
        print("please specify Instance as first argv param")
        sys.exit(2)
    instance = sys.argv[1]
    connection = pymysql.connect(host=settings['host'], port=settings['port'],cursorclass=pymysql.cursors.DictCursor,connect_timeout=settings['connect_timeout']) #how to set timeout?!
    while True:
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SHOW STATUS"
                cursor.execute(sql)
                resultall = cursor.fetchall()
        except:
            print("An exception occurred")
            sys.exit(2)
        newdata=processdata(resultall)
        printvals(newdata,instance=instance)
        time.sleep(interval)

def processdata(statusdata):
    newdata = {}
    for i in statusdata:
        if i['Counter'] in stats['fields']:
            newdata[i['Counter']] = i['Value']
    return(newdata)

if __name__ == '__main__':
    main()
