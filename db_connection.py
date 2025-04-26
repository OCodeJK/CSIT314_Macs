import psycopg2
from psycopg2 import pool

class DatabaseConnection:
    __connection_pool = None
    
    @classmethod
    def initialize(cls, minconn=1, maxconn=10, **kwargs):
        cls.__connection_pool = pool.ThreadedConnectionPool(minconn, maxconn, **kwargs)
    
    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn()
    
    @classmethod
    def return_connection(cls, connection):
        cls.__connection_pool.putconn(connection)
    
    @classmethod
    def close_all_connections(cls):
        cls.__connection_pool.closeall()

class ConnectionFromPool:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = DatabaseConnection.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        DatabaseConnection.return_connection(self.connection)