import psutil
import mysql.connector
from datetime import datetime
import time

#function to collect and store process information
def get_process_info():
    try:
        #Establish connection to database
        conn = mysql.connector.connect(user='root', password='password', host='localhost', database='process')
        cursor_conn = conn.cursor()

        for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info', 'num_threads', 'ppid', 'status', 'create_time']):
            info = proc.info
            pid = info['pid']
            name = info['name']
            memory_info = info.get('memory_info')  # Get the memory_info dictionary safely

            if memory_info:
                rss = memory_info.rss
                vms = memory_info.vms
            else:
                rss = vms = None

            num_threads = info['num_threads']
            ppid = info['ppid']
            status = info['status']
            create_time = datetime.fromtimestamp(info['create_time']).strftime('%Y-%m-%d %H:%M:%S')  # Convert to readable date format

            # Define SQL query with placeholders
            insert_query = """
                           INSERT INTO process_monitor(pid, name, rss, vms, num_threads, ppid, status, create_time)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

            cursor_conn.execute(insert_query, (pid, name, rss, vms, num_threads, ppid, status, create_time))

        # Commit changes to the database
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close connections
        cursor_conn.close()
        conn.close()

def get_memory_info():
    try:
        #Establish connection to database
        conn = mysql.connector.connect(user='root', password='password', host='localhost', database='process')
        cursor_conn = conn.cursor()
        
        
        mem_info = psutil.virtual_memory()
        swap_info = psutil.swap_memory()
        sys_uptime = datetime.fromtimestamp(psutil.boot_time()) #retrieve system uptime
               
        #Memory metrics to be retrieved
        total_memory= mem_info.total
        available_memory = mem_info.available
        used_memory = mem_info.used
        total_swap = swap_info.total
        used_swap = swap_info.used
        free_swap =swap_info.free
        system_uptime =sys_uptime
        
        #Define SQL query with placeholders
        insert_query = """
                      INSERT INTO memory_usage(total_mem, available_mem, used_mem, total_swap, used_swap, free_swap, system_uptime)
                      VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        cursor_conn.execute(insert_query, (total_memory, available_memory, used_memory, total_swap, used_swap, free_swap,system_uptime))

           #Commit changes to the database
        conn.commit()
           
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        
        # Close connections
        cursor_conn.close()
        conn.close()
    

get_process_info()
get_memory_info()





