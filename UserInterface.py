from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QMenu, QMenuBar, QHeaderView, QComboBox, QWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QAction
import sys
import mysql.connector

class CustomTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(13)  # Set the number of columns
        self.setHorizontalHeaderLabels(["PID", "PPID", "NAME", "CPU_PERCENT", "WSET", "PEAK_WSET", "PFILES", "PEAK_PFILES", "NUM_PFAULTS", "PRIVATE", "STATUS", "CREATE_TIME", "TIME_STAMP"])

    def populate_table(self, data):
        self.setRowCount(0)
        for row_num, row_data in enumerate(data):
            self.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.setItem(row_num, col_num, item)


def proc_display():
    try:
       #Connect to database
       conn = mysql.connector.connect(user='root', password='password', host='localhost', database='process')
       cursor_conn = conn.cursor()

       #Querying the database for 
       cursor_conn.execute("""
                           SELECT PID, PPID, NAME, CPU_PERCENT, WSET, PEAK_WSET, PFILES, PEAK_PFILES, NUM_PFAULTS, PRIVATE, STATUS, CREATE_TIME, TIME_STAMP   
                           FROM process_monitor
                           """)
       proc_info = cursor_conn.fetchall()

       #close the database connection
       cursor_conn.close()
       conn.close()
      
       # Update the custom table widget with the new data
       table.populate_table(proc_info)
   
    except mysql.connector.Error as ex:
       print(f"Error: {ex}")


app = QApplication(sys.argv)
main_window = QMainWindow()
main_window.setWindowTitle("Memory Resource Monitor")
main_window.setGeometry(100,100,2000,800)

table = CustomTableWidget(main_window)
table.setGeometry(100,50,1350,700)

#Timer for the user interface to be updated in intervals
interval = QTimer()
interval.timeout.connect(proc_display)
interval.start(10000) #10 seconds interval

main_window.show() #To ensure the window gets displayed


sys.exit(app.exec()) #the code stops running once the window is closed