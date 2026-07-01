import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(
    dbname='your_db',
    user='your_user',
    password='your_pass',
    host='your_host',
    port='your_port'
)

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cursor = conn.cursor()

try:
    cursor.execute("CREATE DATABASE sales_db;")
    print("Database 'sales_db' created successfully!")
except psycopg2.errors.DuplicateDatabase:
    print("Database 'sales_db' already exists.")

cursor.close()
conn.close()
