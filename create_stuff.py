import getpass
import sqlite3
from werkzeug.security import generate_password_hash
from database import init_databases, insert_staff

init_databases()
number = input("Membership number: ").strip()
password = getpass.getpass("Password: ")

try:
    insert_staff(number, generate_password_hash(password))
    print("Staff account created.")
except sqlite3.IntegrityError:
    print("That membership number already exists.")