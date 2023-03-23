from database import Database

def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

def connect_to_default_db():
    db = Database()
    conn = db.create_connection(
        "postgres", "postgres", "postgres", "127.0.0.1",
    )
    return db

def connect_to_db(database_name):
    db = Database()
    conn = db.create_connection(
        database_name, "postgres", "postgres", "127.0.0.1",
    )
    return db


def create_database(database_name):
    db = connect_to_default_db()
    db.create_database(database_name)
    db.close()

def create_table(database_name, table_name):
    db = connect_to_db(database_name)
    db.create_table(table_name)
    db.close()

def get_column_name(database_name, table_name):
    db = connect_to_db(database_name)
    column_names = db.get_column_names(table_name)
    db.close()
    return column_names