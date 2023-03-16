import sqlite3
from contextlib import ContextDecorator


class DatabaseConnection(ContextDecorator):
    def __init__(self, database_name):
        self.database_name = database_name

    def __enter__(self):
        self.sqlite_connection = sqlite3.connect(self.database_name)
        return self.sqlite_connection.cursor()

    def __exit__(self, *exc):
        if self.sqlite_connection:
            self.sqlite_connection.close()


class TableManager:
    conn = DatabaseConnection

    def __init__(self, table_name, db, **kwargs):
        self.db = db
        self.table_name = table_name
        self.types = kwargs
        self.foreign_keys = []
        self.column_names = []
        for key, val in self.types.items():
            if isinstance(val, str):
                self.types[key] = val.upper()
            elif hasattr(val, 'table_name'):
                self.types[key] = 'INTEGER'
                self.foreign_keys.append(
                    f'FOREIGN KEY({key}) REFERENCES {val.table_name}(id)')
            else:
                raise TypeError

        with self.conn(self.db) as db:
            pass

    def create_table(self):
        vals = ', '.join([f'{key} {val}' for key, val in self.types.items()])
        foreigns = ', ' + \
            ', '.join(self.foreign_keys) if self.foreign_keys else ''
        command = f'CREATE TABLE IF NOT EXISTS {self.table_name} ( id INTEGER PRIMARY KEY, {vals}{foreigns})'
        with self.conn(self.db) as db:
            db.executescript(command)

        return self

    def to_dict(self, values):
        if not values:
            return None
        
        return {key: value for key, value in zip(('id', *list(self.types.keys())), values)}

    def to_dict_many(self, query_result):
        if not query_result:
            return [] 
        return [self.to_dict(values) for values in query_result]

    def insert(self, **kwargs):
        colums = ', '.join([f'"{key}"' for key in kwargs.keys()])
        values = ', '.join([f'"{val}"' for val in kwargs.values()])
        command = f'INSERT INTO {self.table_name} ({colums}) values({values});'
        with self.conn(self.db) as db:
            db.executescript(command)

        return self

    def select_all(self):
        with self.conn(self.db) as db:
            db.execute(f'SELECT * FROM {self.table_name};')
            return self.to_dict_many(db.fetchall())

    def select_when_id_greater(self, id):
        with self.conn(self.db) as db:
            db.execute(f'SELECT * FROM {self.table_name} WHERE id>{id};')
            return self.to_dict_many(db.fetchall())

    def select(self, *args, **kwargs):
        conds = ' AND '.join([f'{cond}' for cond in args])
        args = ' AND '.join(['{} = {!r}'.format(k, v)
                             for k, v in kwargs.items()])
        command = f'SELECT * FROM {self.table_name} WHERE {args}{conds};'
        with self.conn(self.db) as db:
            db.execute(command)
            return self.to_dict(db.fetchone())

    def select_many(self, *args, **kwargs):
        conds = ' AND '.join([f'{cond}' for cond in args])
        args = ' AND '.join(['{} = {!r}'.format(k, v)
                             for k, v in kwargs.items()])
        command = f'SELECT * FROM {self.table_name} WHERE {args}{conds};'
        with self.conn(self.db) as db:
            db.execute(command)
            return self.to_dict_many(db.fetchall())

    def update(self, new_data: dict, **kwargs):
        values = ', '.join(['{} = "{}"'.format(k, v)
                            for k, v in new_data.items()])
        cond = ' AND '.join(['{}.{} = {!r}'.format(self.table_name, k, v)
                             for k, v in kwargs.items()])
        command = f'UPDATE {self.table_name} SET {values} WHERE {cond};'
        with self.conn(self.db) as db:
            db.executescript(command)

    def delete(self, *args, **kwargs):
        conds = ' AND '.join([f'{cond}' for cond in args])
        args = ' AND '.join(['{} = {!r}'.format(k, v)
                             for k, v in kwargs.items()])
        command = f'DELETE FROM {self.table_name} WHERE {args}{conds};'
        with self.conn(self.db) as db:
            db.executescript(command)


# class Message(TableManager):
#     table_name = 'messages'

#     def __init__(self, db):
#         super().__init__(
#             table_name=self.table_name,
#             db=db,
#             user='TEXT',
#             message='TEXT',
#             date='TEXT'
#         )

#     def append(self, data):
#         self.insert(**data)

#     def __len__(self):
#         return len(self.select_all())

#     def get_after(self, index):
#         return self.select_when_id_greater(index)
