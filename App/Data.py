#!/usr/bin/env python3

import sqlite3


def to_lower(t):
    return t.lower()


class Data:
    db = None

    @classmethod
    def init(cls, file):
        cls.db = sqlite3.connect(file)
        cls.db.create_function('to_lower', 1, to_lower)

    @classmethod
    def make_table(cls):
        cur = cls.db.cursor()
        cur.execute("create table items (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                    "cell INTEGER, title VARCHAR, quantity INTEGER, description TEXT)")

    @classmethod
    def find(cls, text):
        """Show items that contains this word
        >>> Data.find('name')
        :param str text:
        :return list:
        """
        cur = cls.db.cursor()
        if text:
            cur.execute("SELECT id, cell, title, quantity FROM items WHERE to_lower(title) LIKE :text OR "
                        "to_lower(description) LIKE :text", {'text': '%' + text.lower() + '%'})
        else:
            cur.execute("SELECT id, cell, title, quantity FROM items LIMIT 100")
        cls.db.commit()

        result = []
        for row in cur.fetchall():
            result.append((int(row[0]), row[1], row[2], row[3]))

        return result

    @classmethod
    def create(cls, data):
        """Add new item
        >>> Data.create({'cell': 1, 'title': 'Name', 'quantity': 2, 'description': ''})
        :param dict data:
        :return bool:
        """
        cur = cls.db.cursor()
        cur.execute("INSERT INTO items(cell, title, quantity, description)"
                    " VALUES(:cell, :title, :quantity, :description)", data)

        return cls.db.commit()

    @classmethod
    def read(cls, id):
        """Returns item with this id
        >>> Data.read(2)
        :param int id:
        :return tuple:
        """
        cur = cls.db.cursor()
        cur.execute("SELECT * FROM items WHERE id = :id", {'id': id})
        cls.db.commit()

        row = cur.fetchone()
        if row is None:
            return None

        return int(row[0]), row[1], row[2], row[3], row[4]

    @classmethod
    def update(cls, data):
        """
        >>> Data.update({'id': 1, 'cell': 1, 'title': 'New', 'quantity': 2, 'description': 'New'})
        :param dict data:
        :return bool:
        """
        cur = cls.db.cursor()
        cur.execute("UPDATE items SET cell = :cell, title = :title, quantity = :quantity, "
                    "description = :description WHERE id = :id", data)

        return cls.db.commit()

    @classmethod
    def delete(cls, id):
        """Remove item
         >>> Data.delete(1)
        :param int id:
        :return bool:
        """
        cur = cls.db.cursor()
        cur.execute("DELETE FROM items WHERE id = :id", {'id': id})

        return cls.db.commit()


if __name__ == '__main__':
    import sys
    import os.path

    db_name = '../resource/database.db'

    if os.path.isfile(db_name):
        sys.exit()

    Data.init(db_name)
    Data.make_table()
