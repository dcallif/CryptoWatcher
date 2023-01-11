import sqlite3


class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('watcher.db')
        self.create_user_table()
        self.create_crypto_table()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_crypto_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS "CRYPTO" (
                  id INTEGER PRIMARY KEY,
                  name TEXT,
                  ticker TEXT,
                  accountAddress TEXT,
                  amountHeld INTEGER,
                  user_id INTEGER FOREIGNKEY REFERENCES USER(id)
                );
                """
        self.conn.execute(query)

    def create_user_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS "USER" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                created Date default CURRENT_DATE,
                updated Date default CURRENT_DATE
                );
                """
        self.conn.execute(query)


class CryptoWatcherModel:
    table_name = "CRYPTO"

    def __init__(self):
        self.conn = sqlite3.connect('watcher.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def get_by_id(self, _id):
        if type(_id) == int:
            where_clause = f"user_id={_id}"
        else:
            where_clause = f"email='{_id}'"
        return self.list_items(where_clause)

    def get_token(self, item_id, user_id):
        query = f'SELECT id, name, ticker, amountHeld, accountAddress ' \
            f'FROM {self.table_name} ' \
            f'WHERE name = "{item_id}" ' \
            f'AND user_id = {user_id}'
        print(query)
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                   for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        print(result)
        return result

    def create(self, params):
        query = f'INSERT INTO {self.table_name} ' \
                f'(name, ticker, amountHeld, accountAddress, user_id) ' \
                f'values ("{params.get("name")}","{params.get("ticker")}",' \
                f'{params.get("amountHeld")}, "{params.get("accountAddress")}", (SELECT id FROM USER WHERE email = "{params.get("user_email")}"))'
        print(query)
        result = self.conn.execute(query)
        return self.list_items(params.get("user_email"))

    def delete(self, item_id, params):
        query = f"DELETE FROM {self.table_name} " \
                f"WHERE name = '{item_id}'" \
                f" AND user_id = (SELECT id FROM USER WHERE email = '{params.get('user_email')}')"
        print(query)
        self.conn.execute(query)
        return self.list_items(params.get('user_email'))

    def update(self, item_id, user_id, update_dict):
        set_query = ", ".join([f'{column} = "{value}"'
                               for column, value in update_dict.items()])
        query = f"UPDATE {self.table_name} " \
                f"SET {set_query} " \
                f"WHERE name = '{item_id}' " \
                f"AND user_id = {user_id}"
        print(query)
        self.conn.execute(query)
        return self.get_token(item_id, user_id)

    def list_items(self, user_id):
        query = ""
        if type(user_id) == int:
            query = f"SELECT name, ticker, amountHeld, accountAddress, user_id " \
                    f"from {self.table_name} " \
                    f"WHERE user_id = {user_id}"
        else:
            query = f"SELECT name, ticker, amountHeld, accountAddress, user_id " \
                    f"from {self.table_name} " \
                    f"WHERE user_id = (SELECT id FROM USER WHERE email = '{user_id}')"
        print(query)
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                   for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        print(result)
        return result


class UserModel:
    table_name = "USER"

    def __init__(self):
        self.conn = sqlite3.connect('watcher.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def get_by_id(self, _id):
        if type(_id) == int:
            return self.list_items(f"WHERE id = {_id}")
        else:
            return self.list_items(f"WHERE email = '{_id}'")

    def get_by_email(self, email):
        query = f"SELECT id, name, email, password, updated " \
                f"from {self.table_name} " \
                f"WHERE email = '{email}'"

        result_set = self.conn.execute(query).fetchone()
        return result_set

    def create(self, email, name, password):
        query = f'INSERT INTO {self.table_name} ' \
                f'(name, email, password) ' \
                f'values ("{name}","{email}","{password}")'
        result = self.conn.execute(query)
        return self.get_by_id(result.lastrowid)

    def list_items(self, where_clause=""):
        query = f"SELECT id, name, email, password, updated " \
                f"from {self.table_name} " + where_clause
        print(query)
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                   for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        print(result)
        return result

    def get_pass(self, _id):
        query = f"SELECT password FROM {self.table_name}" \
                f"WHERE id = {_id}"
        print(query)
        result_set = self.conn.execute(query).fetchone()
        return result_set

    def get_id(self, email):
        query = f"SELECT id FROM {self.table_name}" \
                f"WHERE id = {email}"
        print(query)
        result_set = self.conn.execute(query).fetchone()
        return result_set
