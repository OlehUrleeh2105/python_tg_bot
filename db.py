import sqlite3


class DB:
    def __init__(self):
        self._connect = sqlite3.connect("base.db", check_same_thread=False)
        self._cursor = self._connect.cursor()
        self._cursor.execute(f"""CREATE TABLE IF NOT EXISTS labs (id integer primary key autoincrement, number, 
      variant, teacher, specs, disc, url)""")


class Labs(DB):
    TABLE_NAME = 'labs'

    def set_data(self, number, variant, teacher, specs, disc, url):
        self._cursor.execute(f"""INSERT INTO {self.TABLE_NAME} VALUES (NULL,?,?,?,?,?,?)""",
                             (number, variant, teacher, specs, disc, url,))
        self._connect.commit()

    def get_all_teacher(self):
        new_data = []
        self._cursor.execute(f"""SELECT teacher FROM {self.TABLE_NAME}""")
        data = self._cursor.fetchall()
        for x in data:
            new_data.append(x[0])
        return list(set(new_data))

    def get_all_number(self, teacher, disc, specs):
        new_data = []
        self._cursor.execute(f"SELECT number FROM {self.TABLE_NAME} WHERE teacher=? AND disc=? AND specs=?",
                             (teacher, disc, specs,))
        data = self._cursor.fetchall()
        for x in data:
            new_data.append(x[0])
        return list(set(new_data))

    def get_all_variant(self, teacher, disc, specs, number):
        new_data = []
        self._cursor.execute(
            f"SELECT variant FROM {self.TABLE_NAME} WHERE teacher=? AND disc=? AND specs=? AND number=?",
            (teacher, disc, specs, number,))
        data = self._cursor.fetchall()
        for x in data:
            new_data.append(x[0])
        return list(set(new_data))

    def get_all_specs(self, teacher, disc):
        new_data = []
        self._cursor.execute(f"SELECT specs FROM {self.TABLE_NAME} WHERE teacher=? AND disc=?", (teacher, disc,))
        data = self._cursor.fetchall()
        for x in data:
            new_data.append(x[0])
        return list(set(new_data))

    def get_all_disc(self, teacher):
        new_data = []
        self._cursor.execute(f"SELECT disc FROM {self.TABLE_NAME} WHERE teacher=?", (teacher,))
        data = self._cursor.fetchall()
        for x in data:
            new_data.append(x[0])
        return list(set(new_data))

    def get_url(self, teacher, specs, disc, number, variant):
        new_data = []
        self._cursor.execute(
            f"SELECT url FROM {self.TABLE_NAME} WHERE teacher=? AND disc=? AND specs=? AND number=? AND variant=?",
            (teacher, disc, specs, number, variant,))
        data = self._cursor.fetchall()
        for x in data:
            new_data.append(x[0])
        return list(set(new_data))


DB()
