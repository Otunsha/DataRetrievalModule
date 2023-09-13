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

        #while loop to implement continouos data retrieval for real time monitoring
        while True:
         for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info', 'ppid', 'status', 'create_time']):
            info = proc.info
            pid = info['pid']
            name = info['name']
            memory_info = info.get('memory_info')  # Get the memory_info dictionary safely

            if memory_info:
                rss = memory_info.rss
                vms = memory_info.vms
                peak_wset = memory_info.peak_wset
                wset = memory_info.wset
            else:
                rss = vms = peak_wset = wset = None

            ppid = info['ppid']
            status = info['status']
            create_time = datetime.fromtimestamp(info['create_time']).strftime('%Y-%m-%d %H:%M:%S')  # Convert to readable date format

            #CPU Usage for each process
            cpu_percent = proc.cpu_percent(interval= 1)

            #timestamp to indicate when data is inserted into the database
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Define SQL query with placeholders
            insert_query = """
                           INSERT INTO process_monitor(pid, name, rss, vms, peak_wset, wset, ppid, status, create_time, cpu_percent, timestamp)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"""

            cursor_conn.execute(insert_query, (pid, name, rss, vms, peak_wset, wset, ppid, status, create_time, cpu_percent, timestamp))

            # Commit changes to the database
            conn.commit()
             # Sleep for a specified time interval (30 seconds) before collecting data again
            time.sleep(30)
    except KeyboardInterrupt as e:
        print(f"An error occurred: {e}")
    finally:
        # Close connections
        cursor_conn.close()
        conn.close()

get_process_info()


