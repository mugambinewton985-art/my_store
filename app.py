from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session

# Sample products
products = [
    {"id": 1, "name": "Laptop", "price": 50000, "description": "High performance laptop"},
    {"id": 2, "name": "Phone", "price": 20000, "description": "Latest smartphone"},
    {"id": 3, "name": "Headphones", "price": 5000, "description": "Noise cancelling headphones"}
]

# Home page showing products
@app.route('/')
def index():
    return render_template('index.html', products=products)

# Product details page
@app.route('/product/<int:product_id>')
def product(product_id):
    product_item = next((p for p in products if p["id"] == product_id), None)
    return render_template('product.html', product=product_item)

# Add to cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append(product_id)
    return redirect(url_for('cart'))

# View cart
@app.route('/cart')
def cart():
    if "cart" not in session or len(session["cart"]) == 0:
        cart_items = []
        total = 0
    else:
        cart_items = [next(p for p in products if p["id"] == pid) for pid in session["cart"]]
        total = sum(item["price"] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

# Checkout
@app.route('/checkout', methods=['POST'])
def checkout():
    session.pop("cart", None)  # Clear cart
    return "<h1>Thank you for your purchase!</h1>"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

@app.route('/')
def index():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template('index.html', products=products)
@app.route('/admin')
def admin():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template('admin.html', products=products)
@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    price = request.form['price']
    description = request.form['description']

    conn = get_db()
    conn.execute(
        "INSERT INTO products (name, price, description) VALUES (?, ?, ?)",
        (name, price, description)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('admin'))
@app.route('/delete_product/<int:id>')
def delete_product(id):
    conn = get_db()
    conn.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))
@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = get_db()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

        conn.execute("""
            UPDATE products
            SET name = ?, price = ?, description = ?
            WHERE id = ?
        """, (name, price, description, id))

        conn.commit()
        conn.close()
        return redirect(url_for('admin'))

    product = conn.execute("SELECT * FROM products WHERE id = ?", (id,)).fetchone()
    conn.close()

    return render_template('edit_product.html', product=product)
@app.route('/order/<int:product_id>', methods=['POST'])
def order(product_id):
    conn = get_db()

    product = conn.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    customer_name = request.form['customer_name']
    phone = request.form['phone']
    quantity = request.form['quantity']

    conn.execute("""
        INSERT INTO orders (product_name, quantity, customer_name, phone)
        VALUES (?, ?, ?, ?)
    """, (product['name'], quantity, customer_name, phone))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))
@app.route('/orders')
def orders():
    conn = get_db()
    orders = conn.execute("SELECT * FROM orders").fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)
@app.route('/admin')
def admin():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template('admin.html', products=products)
@app.route('/sitemap.xml')
def sitemap():
    return """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://my-store-q0gw.onrender.com/</loc>
    </url>
</urlset>""", 200, {'Content-Type': 'application/xml'}
@app.route('/dashboard')
def dashboard():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template('dashboard.html', products=products)
