import os
import sqlite3
from werkzeug.security import generate_password_hash
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
os.makedirs(DB_DIR, exist_ok=True)

#===========connect to busness.db===========
def get_connection_business():
    connection = sqlite3.connect(os.path.join(DB_DIR, "business.db"))
    connection.row_factory = sqlite3.Row
    return connection

#===========connect to staff.db===========
def get_connection_staff():
    connection = sqlite3.connect(os.path.join(DB_DIR, "staff.db"))
    connection.row_factory = sqlite3.Row
    return connection

#============Used once to create database and table====
def create_database_business():
    connection = get_connection_business()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            second_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            hash_password TEXT NOT NULL,
            message TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending'
        )
    """)
    connection.commit()
    connection.close()


#============Used once to create database of staff and table
def create_database_staff():
    connection = get_connection_staff()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS staff_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            membership_number TEXT NOT NULL UNIQUE,
            hash_password TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()
#create_database_business()
#create_database_staff()

def init_databases():
    create_database_business()
    create_database_staff()


#==========When user register it run=================
def insert_customers(first_name, second_name, last_name, email,
                     hash_password, message, category, priority):
    connection = get_connection_business()
    try:
        connection.execute("""
            INSERT INTO customers(first_name, second_name, last_name, email,
                                  hash_password, message, category, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (first_name, second_name, last_name, email,
              hash_password, message, category, priority))
        connection.commit()
    finally:
        connection.close()

# ============== Staff na admin,(hawana html ya kuregister wanawekwa kwenye mfumo manually)  ========
def insert_staff(membership_number,
                     hash_password):
    connection = get_connection_staff()
    try:
        hash_password = generate_password_hash(hash_password)
        connection.execute("""
            INSERT INTO staff_details(membership_number,hash_password)
            VALUES (?, ?)
        """, (membership_number,
              hash_password,))
        connection.commit()
        print(membership_number, "Inserted ", hash_password)
    finally:
        connection.close()

#insert_staff("yoeli", "siwiti")

def get_customer_by_email(email):
    connection = get_connection_business()
    row = connection.execute(
        "SELECT * FROM customers WHERE email = ?", (email,)).fetchone()
    connection.close()
    return row

def get_customer_by_name(email):
    connection = get_connection_business()
    row = connection.execute(
        "SELECT * FROM customers WHERE email = ?", (email,)).fetchone()
    connection.close()
    return row


def get_customer_by_id(customer_id):
    connection = get_connection_business()
    row = connection.execute(
        "SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
    connection.close()
    return row


def get_all_customers():
    connection = get_connection_business()
    rows = connection.execute("SELECT * FROM customers ORDER BY id DESC").fetchall()
    connection.close()
    return rows


def get_stats():
    connection = get_connection_business()
    total = connection.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    pending = connection.execute(
        "SELECT COUNT(*) FROM customers WHERE status = 'Pending'").fetchone()[0]
    high = connection.execute(
        "SELECT COUNT(*) FROM customers WHERE priority = 'High'").fetchone()[0]
    connection.close()
    return total, pending, high


def get_staff_by_membership(membership_number):
    connection = get_connection_staff()
    row = connection.execute(
        "SELECT * FROM staff_details WHERE membership_number = ?",
        (membership_number,)).fetchone()
    connection.close()
    return row