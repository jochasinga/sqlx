import typer
import pickle
import os
import app
import gpt
from database import DatabaseInfo
from rich import print as pprint
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from prompt import Prompt as GPTPrompt


cli = typer.Typer()


def load_db_info():
    if os.path.exists("db_info.pkl"):
        return pickle.load(open("db_info.pkl", "rb"))
    return None


def save_db_info(db_info):
    pickle.dump(db_info, open("db_info.pkl", "wb"))


@cli.command()
def disconnect():
    app.close_db()
    save_db_info(DatabaseInfo())


@cli.command()
def info():
    db_info = load_db_info()
    app.connect_to_db(db_info.name, db_info.user, db_info.password, db_info.host, db_info.url)
    table = Table(title="Database Info")
    columns = ["name", "user", "password", "host", "url"]
    for col in columns:
        table.add_column(col, justify="right", style="cyan", no_wrap=True)

    if db_info is not None:
        table.add_row(
            db_info.name, db_info.user, db_info.password, db_info.host, db_info.url,
        )

    console = Console()
    console.print(table)


'''
@cli.command()
def table_names():
    db_info = load_db_info()
    app.connect_to_db(db_info.name, db_info.user, db_info.password, db_info.host, db_info.url)
    table_names = app.get_table_names()
    columns = Columns(table_names, equal=True, expand=True)
    pprint(columns)
'''


@cli.command()
def describe(table_name: str):
    db_info = load_db_info()
    app.connect_to_db(db_info.name, db_info.user, db_info.password, db_info.host, db_info.url)
    properties = app.get_column_properties(table_name)
    table = Table(title=table_name)
    column_names = [
        "column_name",
        "data_type",
        "is_nullable",
        "column_default",
    ]

    for col in column_names:
        table.add_column(col, justify="right", style="cyan", no_wrap=True)

    for prop in properties:
        table.add_row(*list(prop))

    console = Console()
    console.print(table)


@cli.command()
def prompt():
    db_info = load_db_info()
    app.connect_to_db(db_info.name, db_info.user, db_info.password, db_info.host, db_info.url)
    prompt = GPTPrompt()
    table_names = app.get_table_names()
    for table in table_names:
        prompt.add_table(table, app.get_column_names(table))

    instruction = Prompt.ask("Your prompt")
    prompt.add_instruction(instruction)
    sql_str = gpt.get_sql(prompt)
    results = app.query(sql_str)

    if results is not None:
        table = Table(title=sql_str)
        column_names = results[0]

        for col in column_names:
            table.add_column(col, justify="right", style="cyan", no_wrap=True)

        for result in results[1:]:
            items = [str(item) for item in list(result)]
            table.add_row(*items)

        console = Console()
        console.print(table)
    else:
        pprint("Transaction successful.")


@cli.command()
def connect(url: str|None = None):
    if url is not None:
        save_db_info(DatabaseInfo(url=url))
    else:
        db_name = Prompt.ask(
            "What is the database name?",
            default="postgres",
        )
        db_user = Prompt.ask(
            "What is the database user?",
            default="postgres",
        )
        db_password = Prompt.ask(
            "What is the database password?",
            default="postgres",
        )
        db_host = Prompt.ask(
            "What is the database host?",
            default="localhost"
        )
        print(f"Connecting to {db_name}")
        save_db_info(DatabaseInfo(db_name, db_user, db_password, db_host, url))


if __name__ == "__main__":
    cli()