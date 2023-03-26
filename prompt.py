class Prompt():
    prompt = "### Postgres SQL tables, with their properties:\n#\n"

    def add_table(self, table_name: str, columns: list[str]):
        column_names = ", ".join(columns)
        self.prompt += f"# { table_name }({ column_names })\n"

    def add_instruction(self, instruction: str):
        self.prompt += "#\n"
        self.prompt += f"### A query to { instruction }\n"
        # self.prompt += "SELECT"

    def get_prompt(self):
        return self.prompt