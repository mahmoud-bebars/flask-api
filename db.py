import sqlite3, random, datetime
from models import Lang
from data import data


def getNewId():
    return random.getrandbits(28)


def connect():
    conn = sqlite3.connect("langs.db")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS langs (id INTEGER PRIMARY KEY, name TEXT,released_year INTEGER,github_rank INTEGER,link TEXT,thumbnail TEXT,description TEXT, timestamp TEXT)"
    )
    conn.commit()
    conn.close()
    for i in data:
        lg = Lang(
            getNewId(),
            i["name"],
            i["released_year"],
            i["githut_rank"],
            i["link"],
            i["thumbnail"],
            i["description"],
        )


def insert(lang):
    conn = sqlite3.connect("langs.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO langs VALUES (?,?,?,?,?,?,?)",
        (
            lang.id,
            lang.name,
            lang.released_year,
            lang.github_rank,
            lang.link,
            lang.thumbnail,
            lang.description,
        ),
    )
    conn.commit()
    conn.close()


def view():
    conn = sqlite3.connect("langs.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM langs")
    rows = cur.fetchall()
    langs = []
    for i in rows:
        lang = Lang(i[0], True if i[1] == 1 else False, i[2], i[3])
        langs.append(lang)
    conn.close()
    return langs


def update(book):
    conn = sqlite3.connect("langs.db")
    cur = conn.cursor()
    cur.execute(
        "UPDATE langs SET name TEXT,name=?, released_year=?,github_rank=?, link=? ,thumbnail=?,description=?, WHERE id=?",
        (book.available, book.title, book.id),
    )
    conn.commit()
    conn.close()


def delete(theId):
    conn = sqlite3.connect("langs.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM langs WHERE id=?", (theId,))
    conn.commit()
    conn.close()


def deleteAll():
    conn = sqlite3.connect("langs.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM langs")
    conn.commit()
    conn.close()
