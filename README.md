# litefast

A more user-friendly alternative to psql CLI. What psql could have been. Make database accessible to everyone.

## Commands

### connect [--url]

Connect to a PostgreSQL database using a URL string or name, user, password, and host.

### disconnect

Forget the PostgreSQL database previously saved.

### describe [TABLE_NAME]

Show the `column_name`, `data_type`, `is_nullable`, and `column_default` of a table's column(s).

```shell
litefast describe account
```

### prompt (beta)

Convert a query in natural language to SQL query and show the formatted result table.

```shell
litefast prompt
Your prompt: list all accounts
```

To use this, you need to have an API key from [OpenAI](openai.com). Create an `.env` file with `OPENAI_API_KEY` variable and place it in the top-level directory.
