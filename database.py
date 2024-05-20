import pyodbc

class DatabaseConnection:
    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                   'SERVER=DESKTOP-VIKK52P;'
                                   'DATABASE=Library;'
                                   'Trusted_Connection=yes;')
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.cursor.close()
