from connect_db import conn, cur

allowed_actions_list = ["Взяти", "Покласти", "Показати загальну кількість", "Додати новий предмет", "Видалити предмет", "Додати користувача"] # actions to do

def get_element_quantity(section, title): 
    number_cur = cur.execute("SELECT Quantity FROM " + section + " WHERE Name = ?;", (title,))
    number = number_cur.fetchone()
    return number[0]

def update_element_quantuty_put(section, title, original_quantity, quantity): # func to increase quantity for already existing in sql object
    new_quantity = original_quantity + quantity
    data = [new_quantity, title]   
    cur.execute("UPDATE " + section +" SET Quantity = ? WHERE Name = ?;", data) 
    conn.commit()
    number_cur = cur.execute("SELECT Quantity FROM " + section + " WHERE Name = ?;", (title,))
    number = number_cur.fetchone()
    return number[0]

def update_element_quantuty_take(section, title, original_quantity, quantity): # func to decrease quantity for already existing in sql object
    new_quantity = original_quantity - quantity
    data = [new_quantity, title]   
    cur.execute("UPDATE " + section + " SET Quantity = ? WHERE Name = ?;", data) 
    conn.commit()
    number_cur = cur.execute("SELECT Quantity FROM " + section + " WHERE Name = ?;", (title,))
    number = number_cur.fetchone()
    return number[0]

def add_new_item(section, wrin, name, quantity, location):
    data = [wrin, name, quantity, location]
    cur.execute("INSERT INTO " + section + " (WRIN, Name, Quantity, Location) VALUES (?, ?, ?, ?);", data)
    conn.commit()
    return "Успішно додано {} в {}.".format(name, section)

def delete_item(section, name):
    data = [name]
    cur.execute("DELETE FROM " + section + " WHERE Name = ?;", data)
    conn.commit()
    return "Успішно видалено {} з {}.".format(name, section)

def get_loc(section, name):
    loc = cur.execute("SELECT Location FROM " + section + " WHERE Name = ?;", (name,))
    location = loc.fetchone()
    return location[0]

