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

def fetch_data():
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
      
       return proc_info
   
    except mysql.connector.Error as ex:
       print(f"Error: {ex}")
       return []

def sort_by_pid():
    table.sortItems(0)

def sort_by_name():
    table.sortItems(2)

app = QApplication(sys.argv)
main_window = QMainWindow()
main_window.setWindowTitle("Memory Resource Monitor")
main_window.setGeometry(100, 100, 2000, 800)

table = CustomTableWidget(main_window)
table.setGeometry(100, 50, 1350, 700)

# Create a menu bar
menu_bar = main_window.menuBar()

# Create a "Sort" menu
sort_menu = QMenu("Sort", main_window)

# Add actions to the "Sort" menu
sort_by_pid_action = QAction("Sort by PID", main_window)
sort_by_pid_action.triggered.connect(sort_by_pid)
sort_menu.addAction(sort_by_pid_action)

sort_by_name_action = QAction("Sort by Name", main_window)
sort_by_name_action.triggered.connect(sort_by_name)
sort_menu.addAction(sort_by_name_action)

# Add the "Sort" menu to the menu bar
menu_bar.addMenu(sort_menu)

# Timer for updating the table
interval = QTimer()
interval.timeout.connect(lambda: table.populate_table(fetch_data()))
interval.start(10000)  # 10 seconds interval

# Initial data population
table.populate_table(fetch_data())

main_window.show()

sys.exit(app.exec())
