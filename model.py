ADMIN_USER="hackbright"
ADMIN_PASSWORD=5980025637247534551
import sqlite3
DB = None
CONN = None
import datetime

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

def authenticate(username, password):
    query = """SELECT id FROM users WHERE username = ? AND password = ?"""
    hashed_pass = hash(password)
    DB.execute(query, (username, hashed_pass))
    row = DB.fetchone()
    print row[0]
    return row[0] #fetching id

    #if username == ADMIN_USER and hash(password) == ADMIN_PASSWORD:
    #    return ADMIN_USER

    return None

def given_name_return_id(username):
    query = """SELECT id FROM users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    return row[0]

def given_id_return_name(user_id):
    query = """SELECT username FROM users WHERE id = ?"""
    DB.execute(query, (user_id,))
    row = DB.fetchone()
    return row[0]

#extracting wallposts
def wall_posts(username):
    query = """SELECT P.*, O.username AS owner_name, A.username AS author_name FROM wall_posts AS P INNER JOIN users AS O ON (P.owner_id = O.id) INNER JOIN users AS A ON (P.author_id = A.id) WHERE O.username = ?"""
    DB.execute(query, (username,))
    rows = DB.fetchall()
    return rows

#username of the owner, id of the author
def add_wall_post(username, author_id, content):
    owner_id = given_name_return_id(username)
    query = """INSERT INTO wall_posts (owner_id, author_id, created_at, content) VALUES (?, ?, ?, ?)"""
    result = DB.execute(query, (owner_id, author_id, datetime.datetime.now(), content))
    CONN.commit()
    print "Post successful! %r " % result

def main():
    # connect_to_db()
    authenticate('hackbright', 'unicorn')
    given_name_return_id('hackbright')
    wall_posts('2')
    # CONN.sqlite3.close()

print "__name__ is ", __name__
if __name__ == "__main__":
    main()