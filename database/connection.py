import psycopg2


class CreateDatabase:
    def __init__(self, user, password, host, port):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def create_database(self, db_name):
        try:
            query = f"CREATE DATABASE {db_name}"
            self.cursor.execute(query)
            print(f"Database {db_name} created successfully")
            return True
        except Exception:
            return False

    def __del__(self):
        self.cursor.close()
        self.connection.close()

class Database:
    def __init__(self, db_name, user, password, host, port):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(query)

    def drop_table(self, table_name):
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(query)

    def insert(self, table_name, columns, values):
        query = f"INSERT INTO {table_name} ({columns}) VALUES (%s, %s, %s)"
        self.cursor.execute(query, values)

    def find(self, table_name, columns, condition):
        query = f"SELECT {columns} FROM {table_name} WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def select(self, table_name):
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update(self, table_name, set, condition):
        query = f"UPDATE {table_name} SET {set} WHERE {condition}"
        self.cursor.execute(query)

    def delete(self, table_name, condition):
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(query)

    # def __del__(self):
    #     self.cursor.close()
    #     self.connection.close()
