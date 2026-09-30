#=================This file determine how message relate to catehory=======


def analyze_message(message):

    message = message.lower()

    #============ Decide category, various words option should be done ===========
    if "payment" in message or "money" in message:
        category = "Payment"

    elif "account" in message or "login" in message:
        category = "Account"

    elif "investment" in message or "invest" in message:
        category = "Investment"

    elif "complaint" in message or "problem" in message:
        category = "Complaint"

    else:
        category = "General"

    #=================== Determine priority, maneno pia
    if "urgent" in message or "problem" in message or "complaint" in message:
        priority = "High"
    else:
        priority = "Normal"

    return category, priority


def reprocess_all_customers():

    from database import get_connection_business

    connection = get_connection_business()

    customers = connection.execute(
        "SELECT * FROM customers"
    ).fetchall()

    for customer in customers:

        category, priority = analyze_message(
            customer["message"]
        )

        connection.execute("""
            UPDATE customers
            SET category = ?, priority = ?
            WHERE id = ?
        """, (category, priority, customer["id"]))

    connection.commit()
    connection.close()
