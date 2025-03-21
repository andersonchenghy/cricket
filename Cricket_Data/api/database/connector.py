from fastapi import HTTPException, status
import os
import mysql.connector
from mysql.connector import Error
import time


class DatabaseConnector:
    def __init__(self):
        for _ in range(5):  # Retry up to 5 times
            try:
                host = os.getenv("DATABASE_HOST", "mysql")
                user = os.getenv("DATABASE_USERNAME", "appuser")
                password = os.getenv("DATABASE_PASSWORD", "P4ssw0rd")
                database = os.getenv("DATABASE", "cricket_data")
                
                print(f"Connecting to database: {database} on host: {host}")
                
                self.conn = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
                )
                self.cursor = self.conn.cursor(dictionary=True)
                return  # Exit if connection is successful
            except Error as e:
                print(f"Error connecting to MySQL: {e}")
                time.sleep(5)  # Wait before retrying
        raise Exception("Could not connect to MySQL after several attempts.")

    def query_get(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error executing query: {e}")
            raise e

    def query_put(self, sql, param):
        try:
            self.cursor.execute(sql, param)
            self.conn.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error executing query: {e}")
            raise e

database = DatabaseConnector()
