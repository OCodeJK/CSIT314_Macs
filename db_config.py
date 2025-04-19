import psycopg2

def db_connection():
    return psycopg2.connect(
        dbname='c2c_db',
        user='help',
        password='1234',
        host='localhost',
        port='5432'
    )