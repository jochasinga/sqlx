import psycopg2
from psycopg2 import OperationalError


class TableField():
    def __init__(
        self, name: str, type: str, unique: bool,
        primary_key: bool, index: bool, not_null: bool,
    ):
        self.name = name
        self.type = type
        self.unique = unique
        self.primary_key = primary_key
        self.index = index
        self.not_null = not_null


class CreateTableConfig():
    def __init__(self, name: str, fields: list[TableField]):
        self.name = name
        self.fields = fields


class DatabaseInfo:
    def __init__(self, name=None, user=None, password=None, host=None, url=None):
        self.name = name
        self.user = user
        self.password = password
        self.host = host
        self.url = url


class Database:

    connection = None
    name: str|None = None
    user: str|None = None
    password: str|None = None
    host: str|None = None
    url: str|None = None


    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.name = None
            self.user = None
            self.password = None
            self.host = None
            self.url = None


    def execute(self, query):
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            if cursor.description is not None:
                colnames = [desc[0] for desc in cursor.description]
                results = [colnames]
                results.extend(cursor.fetchall())
                return results

            return None
        except OperationalError as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()


    def execute_query(self, query):
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except OperationalError as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()


    def create_connection(self, db_name='postgres', db_user='postgres', db_password='postgres', db_host='127.0.0.1', url=None):
        connection = None
        try:
            if url is not None:
                connection = psycopg2.connect(url)
                self.url = url
            else:
                connection = psycopg2.connect(
                    database=db_name, user=db_user, password=db_password, host=db_host
                )
                self.name = db_name
                self.user = db_user
                self.password = db_password
                self.host = db_host
        except OperationalError as e:
            print(f"The error '{e}' occurred")

        self.connection = connection
        return connection


    def create_database(self, database_name: str):
        create_db_query = f"""
        SELECT 'CREATE DATABASE {database_name}'
        WHERE NOT EXISTS (SELECT FROM pg_database
        WHERE datname = '{database_name}')
        """
        # self.execute_query(create_db_query)
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"CREATE DATABASE {database_name}")
        except OperationalError as e:
            print(f"The error '{e}' occurred")


    def get_rows(self, table_name: str, limit: int = 10):
        query = f"""
        SELECT * FROM {table_name} LIMIT {limit}
        """
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    def get_table_names(self, schema: str = 'public'):
        query = f"""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
        AND table_schema = '{schema}'
        """
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except OperationalError as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()

    def get_column_properties(self, table_name: str):
        query = f"""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        """
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except OperationalError as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()


    def get_column_names(self, table_name: str):
        query = f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        """
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except OperationalError as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()

    def create_table(self, table: CreateTableConfig):
        clause = ""
        for i, field in enumerate(table.fields):
            clause += "\n\t\t"
            clause += f"{field.name} {field.type}"
            if field.unique:
                clause += " UNIQUE"
            if field.primary_key:
                clause += " PRIMARY KEY"
            if field.index:
                clause += " INDEX"
            if field.not_null:
                clause += " NOT NULL"

            if i < len(table.fields) - 1:
                clause += ", "

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table.name} (
            {clause}
        )
        """

        self.execute_query(create_table_query)


