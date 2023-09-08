import psutil, datetime
import mysql.connector
        
def get_process_info():
    
    conn = mysql.connector.connect(user='root', password='password', host='localhost', database='process')
    cursor_conn = conn.cursor()

    for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info', 'num_threads', 'ppid', 'status', 'create_time']):
      info = proc.info
      pid = info['pid']
      name = info['name']
      memory_info = info['memory_info']  # Get the memory_info dictionary
      rss = memory_info.rss
      vms = memory_info.vms
      num_page_faults = memory_info.num_page_faults
      wset = memory_info.wset
      peak_wset = memory_info.peak_wset
      num_threads = info['num_threads']
      ppid = info['ppid']
      status = info['status']
      create_time = info['create_time']

      #Define Sql query with placeholders
      insert_query = """
                     INSERT INTO process_monitor(pid,name,rss,vms,num_page_faults,wset,peak_wset,num_threads,ppid,status,create_time)
                     VALUES(%s,%s,%s,%s,%d,%s,%s,%d,%d,%s,%s)"""

      cursor_conn.execute(insert_query, (pid, name, rss,vms,num_page_faults,wset,peak_wset,num_threads,ppid,status,create_time ))
    #Commit changes to the database
      conn.commit()
    
    #Close Connections
      cursor_conn.close()
      conn.close()

get_process_info()