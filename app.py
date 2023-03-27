from database import Database, CreateTableConfig

db = Database()

def query(query: str):
    results = db.execute(query)
    return results

def connect_to_default_db():
    # db = Database()
    db.create_connection(
        "postgres", "postgres", "postgres", "127.0.0.1", url=None
    )
    return db

def connect_to_db(
        name,
        user: str = "postgres",
        password: str = "postgres",
        host: str = "127.0.0.1",
        url: str|None = None,
    ):
    # db = Database()
    db.create_connection(name, user, password, host, url=url)
    return db

def get_current_connection():
    return db.connection

def is_connected():
    if db.connection is not None:
        return db.connection.closed == 0
    else:
        return False

def create_database(database_name):
    # db = connect_to_default_db()
    db.create_database(database_name)
    # db.close()

def create_table(table_config: CreateTableConfig):
    # db = connect_to_db(database_name)
    db.create_table(table_config)
    # db.close()

def get_column_names(table_name):
    # db = connect_to_db(database_name)
    results = db.get_column_names(table_name)
    column_names = [result[0] for result in results]
    # db.close()
    return column_names

def get_column_properties(table_name: str):
    results = db.get_column_properties(table_name)
    return results

def get_table_names(schema: str = 'public'):
    # db = connect_to_db(database_name)
    results = db.get_table_names(schema)
    table_names = [result[0] for result in results]
    # db.close()
    return table_names

def get_tables(schema: str = 'public'):
    results = db.get_tables(schema)
    return results

def close_db():
    db.close()