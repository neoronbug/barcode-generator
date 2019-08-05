import sqlite3


def connect():
    con = sqlite3.connect("barcode_database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS barcode_data(cmp_id INTEGER PRIMARY KEY, product_code text, product_name text,price text)")
    con.commit()
    con.close()


def add_code(code,name,price):
    con = sqlite3.connect("barcode_database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO barcode_data VALUES(NULL,?,?,?)",
                (code,name,price))
    con.commit()
    con.close()


def select_code_data():
    conn = sqlite3.connect("barcode_database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM barcode_data")
    rows = cur.fetchall()
    conn.close()
    return rows

def search_with_code_data(code,product_name):
    conn = sqlite3.connect("barcode_database.db")
    cur = conn.cursor()
    if product_name=='':
        cur.execute("SELECT * FROM barcode_data WHERE product_code=?",(code,))
    elif code=='':
        cur.execute("SELECT * FROM barcode_data WHERE product_name=?",(product_name,))
    rows = cur.fetchone()
    conn.close()
    return rows

connect()