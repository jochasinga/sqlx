import psycopg2
from psycopg2 import OperationalError
import schemas

class Database:

    def __init__(self, db_name='postgres', db_user='postgres', db_password='postgres', db_host='127.0.0.1'):
        self.connection = self.create_connection(db_name, db_user, db_password, db_host)


    def close(self):
        if self.connection:
            self.connection.close()


    def execute_query(self, query):
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Query executed successfully")
        except OperationalError as e:
            print(f"The error '{e}' occurred")


    def create_connection(self, db_name='postgres', db_user='postgres', db_password='postgres', db_host='127.0.0.1'):
        connection = None
        try:
            connection = psycopg2.connect(
                database=db_name, user=db_user, password=db_password, host=db_host
            )
            print(f"Connection to PostgreSQL DB {db_name} successful")
        except OperationalError as e:
            print(f"The error '{e}' occurred")

        self.connection = connection
        return connection


    def create_database(self, database_name):
        create_db_query = f"""
        SELECT 'CREATE DATABASE {database_name}'
        WHERE NOT EXISTS (SELECT FROM pg_database
        WHERE datname = '{database_name}')
        """
        # self.execute_query(create_db_query)
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            # cursor.execute(f"SELECT 'CREATE DATABASE {database_name}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{database_name}')")
            cursor.execute(f"CREATE DATABASE {database_name}")
            print("Query executed successfully")
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    def get_rows(self, table_name, limit=10):
        query = f"""
        SELECT * FROM {table_name} LIMIT {limit}
        """
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Query executed successfully")
            return cursor.fetchall()
        except OperationalError as e:
            print(f"The error '{e}' occurred")


    def get_column_names(self, table_name):
        query = f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        """
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Query executed successfully")
            return cursor.fetchall()
        except OperationalError as e:
            print(f"The error '{e}' occurred")


    def create_table(self, table: schemas.TableCreate):
        clause = ""
        for i, fields in enumerate(table.fields):
            clause += "\n\t\t"
            # type = ""
            # if fields.type == "int" and not fields.serial:
            #     type = "INTEGER"
            # elif fields.type == "int" and fields.serial:
            #     type = "SERIAL"
            # elif fields.type == "str":
            #     type = "TEXT"

            clause += f"{fields.name} {fields.type}"
            if fields.unique:
                clause += " UNIQUE"
            if fields.primary_key:
                clause += " PRIMARY KEY"
            if fields.index:
                clause += " INDEX"
            if fields.not_null:
                clause += " NOT NULL"

            if i < len(table.fields) - 1:
                clause += ", "

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table.name} (
            {clause}
        )
        """
        print('query: ', create_table_query)
        self.execute_query(create_table_query)


