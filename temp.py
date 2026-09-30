import sqlite3

def view():
    connection = sqlite3.connect("C:/Users/yoely/PycharmProjects/Siwiti-Business-Automation/database/business.db")
    cursor = connection.cursor()

    result = cursor.execute("""SELECT * FROM customers WHERE email = ?
    """, ("yoelysiwiti2@gmail.com",)).fetchall()
    connection.close()
    print()

    for res in result:
        print(res)