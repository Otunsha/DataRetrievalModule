import psutil
import mysql.connector
from datetime import datetime
import time


#Function for bytes conversion to megabytes
def convert_bytes(bytes):
    if bytes is None:
        return "Null"
    return f"{bytes/(1024*1024):.2f}MB"

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
                wset = memory_info.wset
                peak_wset = memory_info.peak_wset
                pfiles = memory_info.pagefile
                peak_pfiles = memory_info.peak_pagefile
                num_pfaults = memory_info.num_page_faults
                private = memory_info.private
            else:
                wset = peak_wset = pfiles = peak_pfiles= num_pfaults= private = None

            ppid = info['ppid']
            status = info['status']
            create_time = datetime.fromtimestamp(info['create_time']).strftime('%Y-%m-%d %H:%M:%S')  # Convert to readable date format

            #CPU Usage for each process
            cpu_percent = proc.cpu_percent(interval= 0.1) #with an interval of half a second for accuracy 

            #timestamp to indicate when data is inserted into the database
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            #convert memory metrics to bytes
            wset_mb = convert_bytes(wset)
            peak_wset_mb = convert_bytes(peak_wset)
            pfiles_mb = convert_bytes(pfiles)
            peak_pfiles_mb = convert_bytes(peak_pfiles)
            num_pfaults_mb = convert_bytes(num_pfaults)
            private_mb = convert_bytes(private)
            
            # Define SQL query with placeholders
            insert_query = """
                           INSERT INTO process_monitor(PID, PPID, NAME, CPU_PERCENT, WSET, PEAK_WSET, PFILES, PEAK_PFILES, NUM_PFAULTS, PRIVATE, STATUS, CREATE_TIME,TIME_STAMP)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)"""

            cursor_conn.execute(insert_query, (pid, ppid, name, cpu_percent, wset_mb, peak_wset_mb, pfiles_mb, peak_pfiles_mb, num_pfaults_mb, private_mb, status, create_time,timestamp))

            # Commit changes to the database
            conn.commit()
             # Sleep for a specified time interval (30 seconds) before collecting data again
            time.sleep(30)

    except KeyboardInterrupt as e:  #KeyboardInterrupt
        print(f"An error occurred: {e}")
    finally:
        # Close connections
        cursor_conn.close()
        conn.close()

get_process_info()


