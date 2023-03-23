from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey


class DatabaseBase(BaseModel):
    name: str


class DatabaseConnect(DatabaseBase):
    user: str
    password: str
    host: str


class DatabaseCreate(DatabaseBase):
    pass


class FieldBase(BaseModel):
    name: str
    type: str
    unique: bool
    primary_key: bool
    index: bool
    not_null: bool


class TableField():
    def __init__(self, name, type, unique, primary_key, index, not_null):
        self.name = name
        self.type = type
        self.unique = unique
        self.primary_key = primary_key
        self.index = index
        self.not_null = not_null


class Field(FieldBase):
    pass

    class Config:
        orm_mode = True


class TableBase(BaseModel):
    name: str


class TableCreate(TableBase):
    fields: list[Field]

    class Config:
        orm_mode = True


