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
            return cur.fetchone()  
        

    def yil_toplam(self, date):
        sql = "SELECT result FROM eko WHERE TRIM(Date) = ?"
        row = self.__select_data(sql, (date.strip(),))

        if row:
            return row[0]
        else:
            return None




if __name__ == "__main__":
    db = DB_Manager("degisim.db")
    print(db.yil_toplam("08-2021"))
