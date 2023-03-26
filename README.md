# sqlx

A more user-friendly alternative to psql CLI. What psql could have been. Make database accessible to everyone.

## Commands

### connect [--url]

Set up a PostgreSQL database to connect to using a URL string or name, user, password, and host.

### disconnect

Forget the PostgreSQL database previously saved.

### describe [TABLE_NAME]

Show the `column_name`, `data_type`, `is_nullable`, and `column_default` of a table's column(s).

```shell
sqlx describe account
```

### prompt (beta)

Convert a query in natural language to SQL query and show the formatted result table if available.

```shell
sqlx prompt
Your prompt: list account with username = 'user1'
```

Or inserting:

```shell
sqlx prompt
Your prompt: insert into account where username = 'user4' and email = 'user4@gmail.com'
```

To use this, you need to have an API key from [OpenAI](openai.com). Create an `.env` file with `OPENAI_API_KEY` variable and place it in the top-level directory.
