import psycopg2

def db_connection():
    return psycopg2.connect(
        dbname='c2c_db',
        user='admin',
        password='123',
        host='localhost',
        port='5432'
    )