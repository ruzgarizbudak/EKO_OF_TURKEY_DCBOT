import sqlite3
import os

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def __excutemany(self,sql,data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit

    def __select_data(self, sql, data=()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall() 
 
        

    def yil_toplam(self, date):
        sql = "SELECT result FROM eko WHERE TRIM(Date) = ?"
        row = self.__select_data(sql, (date.strip(),))

        if row:
            return row[0]
        else:
            return None


    def aylik_veri(self, year):
        sql = """
        SELECT Date, CPI_Monthly_Change
        FROM eko
        WHERE substr(Date, 4, 4) = ?
        ORDER BY substr(Date, 1, 2)
        """
        return self.__select_data(sql, (str(year),))






if __name__ == "__main__":
    db = DB_Manager("degisim.db")
    print(db.yil_toplam("08-2021"))
