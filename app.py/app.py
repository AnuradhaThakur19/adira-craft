from flask import Flask, render_template, request
import sqlite3
import os

print("Database Path:", os.path.abspath("database.db"))

app = Flask(__name__)

# Home Page
@app.route("/")
def home():
    return render_template("home.html")


# Products Page
@app.route("/products")
def products():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    conn.close()

    return render_template(
        "product.html",
        products=products
    )


# About Page
@app.route("/about")
def about():
    return render_template("about.html")


# Contact Page
@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO contacts
        (name, email, message)
        VALUES (?, ?, ?)
        """, (name, email, message))

        conn.commit()
        conn.close()

        return """
        <h2>Message Sent Successfully ❤️</h2>
        <a href='/contact'>Back</a>
        """

    return render_template("contact.html")


# Order Page
@app.route("/order", methods=["GET", "POST"])
def order():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]
        product = request.form["product"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO orders
        (customer_name, phone, address, product_name)
        VALUES (?, ?, ?, ?)
        """, (name, phone, address, product))

        conn.commit()
        conn.close()

        return """
        <h2>Order Placed Successfully ❤️</h2>
        <a href='/products'>Back to Products</a>
        """

    return render_template("order.html")



# Owner Dashboard
@app.route("/adira_owner_dashboard_2026")
def admin():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()

    cursor.execute("SELECT * FROM contacts")
    messages = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        orders=orders,
        messages=messages
    )

#message in admin panel
@app.route("/messages")
def messages():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts")

    messages = cursor.fetchall()

    conn.close()

    return render_template(
        "message.html",
        messages=messages
    )



# Run Application
if __name__ == "__main__":
    app.run(debug=True)