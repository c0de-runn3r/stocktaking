import sqlite3

conn = sqlite3.connect('stock.db') # connect to SQLite DB
cur = conn.cursor()

def get_table_list(): # get names of tables in DB
    table_list = []
    tables = cur.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';").fetchall()

    for table in tables:
        table = table[0]
        table_list.append(table)
    return table_list

def get_item_list(table_name): # get names of items in table *name* in DB
    item_list = []
    items = cur.execute("SELECT Name FROM " + table_name +";").fetchall()
    for item in items:
        item = item[0]
        item_list.append(item)
    return item_list

def get_item_list_with_quantity(table_name):
    text = "<strong>Таблиця {}</strong>\n\n".format(table_name)
    items = cur.execute("SELECT Name, Quantity, WRIN FROM " + table_name +";").fetchall()
    for item in items:
       text += "(" + str(item[2]) + ") " + item[0] + " - " + str(item[1]) + "\n"
    return text

