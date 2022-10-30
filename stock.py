from config import LOGIN_WORD
from connect_db import conn, cur

allowed_actions_list = ["Взяти", "Покласти"] # actions to do

def login():   # login func 
    while True:
        word = input("Type your login here: ")
        if word == LOGIN_WORD:
            break
        else:
            print("Login is not correct! Try again.")

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





