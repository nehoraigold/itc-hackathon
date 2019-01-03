import sqlite3
import json

DB_FILE = 'jpark.db'


class MapsDb:
    def __init__(self):

        CREATE_PARK = """CREATE TABLE IF NOT EXISTS Parking (ID INTEGER PRIMARY KEY AUTOINCREMENT,lat DECIMAL(10, 8) 
        NOT NULL,lng DECIMAL(11, 8) NOT NULL, datetime TEXT NOT NULL);"""

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(CREATE_PARK)
        conn.commit()
        c.close()



    def insert_point(self, point):
        """insert a data point """
        sql = ''' INSERT INTO Parking(lat, lng, datetime) VALUES(?,?,?) '''
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(sql, point)
        conn.commit()
        c.close()


if __name__ == '__main__':
    database = MapsDb()

    # database.insert_point()
