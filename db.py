import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("HOST"),
    "user": os.getenv("USER"),
    "password": os.getenv("MYSQL_ROOT_PASSWORD"),
    "database": os.getenv("DATABASE"),
}

def connection_to_database():
    return mysql.connector.connect(**DB_CONFIG)

def create_tables():
    with connection_to_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
               create table IF NOT EXISTS app_status (
                  id int auto_increment primary key,
                  timestamp datetime,
                  app_name varchar(255),
                  status varchar(50),
                  response_time float
               );""")
