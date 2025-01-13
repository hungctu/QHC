import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        # Kiểm tra nếu là câu lệnh SELECT thì cần xử lý kết quả
        if query.strip().lower().startswith("select"):
            result = self.cursor.fetchall()  # Đọc kết quả nếu là câu lệnh SELECT
            print("Result from SELECT:", result)
        self.conn.commit()  # Commit sau mỗi thao tác SQL

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()



