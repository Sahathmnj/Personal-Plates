import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, customer_info, chef_info, login_required, login_administrator_required, login_customer_required, login_chef_required, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    # Query database for Customer
    customer = db.execute(
        "SELECT * FROM customers WHERE username = ?", request.form.get("username")
    )

    chef = db.execute(
        "SELECT * FROM chefs WHERE username = ?", request.form.get("username")
    )

    administrator = db.execute(
        "SELECT * FROM administrator WHERE username = ?", request.form.get("username")
    )

    if len(customer) == 1:
        # Redirect to Custome Home
        return redirect("/customer_home")
    elif len(chef) == 1:
        # Redirect to Chefs Home
        return redirect("/chef_home")
    elif len(administrator) == 1:
        # Redirect to Administrator Home
        return redirect("/administrator_home")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for Customer
        customer = db.execute(
            "SELECT * FROM customers WHERE username = ?", request.form.get("username")
        )

        if len(customer) != 1:
            # Query database for Chefs
            chef = db.execute(
                "SELECT * FROM chefs WHERE username = ?", request.form.get("username")
            )

            # Ensure Chef username exists and password is correct
            if len(chef) != 1 or not check_password_hash(
                chef[0]["hash"], request.form.get("password")
            ):

                return apology("invalid username and/or password", 403)
            else:

                # Remember which Chef has logged in
                session["user_id"] = chef[0]["id"]

                # Redirect user to home page
                return redirect("/chef_home")

        else:

            # Ensure Customer  password is correct
            if not check_password_hash(
                customer[0]["hash"], request.form.get("password")
            ):

                return apology("invalid username and/or password", 403)
            else:

                # Remember which customer has logged in
                session["user_id"] = customer[0]["id"]

                # Redirect user to home page
                return redirect("/customer_home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register_customer", methods=["GET", "POST"])
def register_customer():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        firstname = request.form.get("firstname", None)
        lastname = request.form.get("lastname", None)
        middlename = request.form.get("middlename", None)
        streetnumber = request.form.get("streetnumber", None)
        streetaddress = request.form.get("streetaddress", None)
        city = request.form.get("city", None)
        state = request.form.get("state", None)
        zipcode = request.form.get("zipcode", None)
        country = request.form.get("country", None)
        phonenumber = request.form.get("phonenumber", None)
        emailaddress = request.form.get("emailaddress", None)

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure password is re-confirmed
        elif not confirmation:
            return apology("must confirm password", 400)

        # Ensure password and re-confirmation is same
        elif password != confirmation:
            return apology("password confirmation failed!", 400)

        # Query customers database if username already exists
        rows = db.execute(
            "SELECT * FROM customers WHERE username = ?", username)

        # Ensure username does not exists
        if len(rows) != 0:
            return apology("username already exists", 400)

        # Query chefs database if username already exists
        rows = db.execute(
            "SELECT * FROM chefs WHERE username = ?", username)

        # Ensure username does not exists
        if len(rows) != 0:
            return apology("username already exists", 400)

        # Generate password hash
        password_hash = generate_password_hash(password)

        db.execute("INSERT INTO customers (username,hash,first_name,last_name,middle_name,street_number,street_address,city,state,zip_code,country,phone_number,email_address) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   username, password_hash, firstname, lastname, middlename, streetnumber, streetaddress, city, state, zipcode, country, phonenumber, emailaddress)

        rows = db.execute(
            "SELECT id FROM customers WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/customer_home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register_customer.html")


@app.route("/login_customer", methods=["GET", "POST"])
def login_customer():
    """Log Customer in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM customers WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/customer_home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login_customer.html")


@app.route("/customer_home")
@login_customer_required
def customer_home():
    """Show portfolio of Customer Order"""

    order_amount = 0

    orders = db.execute(
        "SELECT customer_order.id as order_id,customer_order.order_date,item.id item_id,item.item_description,item.price,item.chef_id,concat(chefs.first_name,' ',chefs.last_name) as chef_name,item.delivery_status FROM customer_order INNER JOIN customer_order_items item ON ( customer_order.id = item.order_id ) INNER JOIN chefs ON ( item.chef_id = chefs.id ) WHERE customer_order.customer_id = (?) and delivery_status = 'Pending' order by customer_order.order_date DESC", session.get("user_id"))

    rows = db.execute(
        "SELECT sum(item.price) order_amount FROM customer_order  INNER JOIN customer_order_items item ON ( customer_order.id = item.order_id ) INNER JOIN chefs ON ( item.chef_id = chefs.id ) WHERE customer_order.customer_id = (?) and delivery_status = 'Pending'", session.get("user_id"))

    if len(orders) > 0:
        order_amount = rows[0].get("order_amount")
    else:
        order_amount = 0

    return render_template("customer_home.html", orders=orders, order_total=order_amount)


@app.route("/customer_place_order", methods=["GET", "POST"])
@login_customer_required
def customer_place_order():
    """Customer Place Order."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        food_name = request.form.get("food_name", None)
        zip_code = request.form.get("zip_code", None)
        meat_category = request.form.get("meat_category", None)
        first_name = request.form.get("first_name", None)

        if not food_name and (not zip_code) and (not meat_category) and (not first_name):
            return customer_info("Food selection cannot be empty", 400)

        if food_name:
            chef_foods = db.execute(
                "SELECT distinct id,chef_id,food_name,price FROM chef_menu where food_name LIKE ?", "%" + food_name.strip() +
                "%"
            )

        if zip_code:
            chef_foods = db.execute(
                "SELECT distinct chef_menu.id,chef_menu.chef_id,chef_menu.food_name,chef_menu.price FROM chef_menu INNER JOIN chefs ON (chefs.id = chef_menu.chef_id) where chefs.zip_code =  (?) ", zip_code
            )

        if meat_category:
            chef_foods = db.execute(
                "SELECT distinct id,chef_id,food_name,price FROM chef_menu where meat_category = (?)", meat_category.strip(
                )
            )

        if first_name:
            chef_foods = db.execute(
                "SELECT distinct chef_menu.id,chef_menu.chef_id,chef_menu.food_name,chef_menu.price FROM chef_menu INNER JOIN chefs ON (chefs.id = chef_menu.chef_id) where chefs.first_name LIKE (?) ", "%" + first_name.strip(
                ) + "%"
            )

        session["cart"] = []
        session["customer_cart"] = []
        session["chef_foods"] = chef_foods
        cart = []

        return render_template("display_foods.html", chef_foods=chef_foods, cart=cart)
    else:
        # Query database for list of chefs
        food_names = db.execute(
            "SELECT food_name FROM chef_menu"
        )
        zip_codes = db.execute(
            "SELECT DISTINCT zip_code FROM chefs"
        )
        meat_category = db.execute(
            "SELECT distinct meat_category FROM chef_menu"
        )
        first_names = db.execute(
            "SELECT distinct first_name FROM chefs"
        )
        return render_template("customer_place_order.html", food_names=food_names, zip_codes=zip_codes, meat_category=meat_category, first_names=first_names)


@app.route("/customer_add_cart", methods=["GET", "POST"])
@login_customer_required
def customer_add_cart():
    """Place Order."""

    # Ensure Cart exists
    if 'customer_cart' not in session:
        session["customer_cart"] = []

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        food_id = int(request.form.get("food_id"))
        chef_id = int(request.form.get("chef_id"))
        food_name = request.form.get("food_name")
        price = float(request.form.get("price"))

        if food_id:
            cart_id = len(session.get("customer_cart")) + 1
            food = {"cart_id": cart_id, "id": food_id, "chef_id": chef_id,
                    "food_name": food_name, "price": price}
            session["customer_cart"].append(food)

        return redirect("/customer_add_cart")

    # GET
    cart = session["customer_cart"]

    if (len(session["chef_foods"])) > 0:
        chef_foods = session["chef_foods"]
    else:
        chef_foods = db.execute(
            "SELECT * FROM chef_menu where chef_id = (?)", session["customer_cart"][0].get(
                "chef_id")
        )

    return render_template("display_foods.html", chef_foods=chef_foods, carts=cart)


@app.route("/customer_remove_cart", methods=["GET", "POST"])
@login_customer_required
def customer_remove_cart():
    """Remove Item from Cart """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        cart_id = int(request.form.get("cart_id"))
        chef_id = int(request.form.get("chef_id"))

        if cart_id:
           # Save chef_id in session variable befroe removing Cart dictionary element. It is used to retrieve food menu in GET method in below secion
            session["chef_id"] = chef_id
            session["customer_cart"] = [
                x for x in session["customer_cart"] if (cart_id != x.get("cart_id"))]

        return redirect("/customer_remove_cart")

    # GET
    cart = session["customer_cart"]

    if (len(session["chef_foods"])) > 0:
        chef_foods = session["chef_foods"]
    else:
        chef_foods = db.execute(
            "SELECT * FROM chef_menu where chef_id = (?)", session["chef_id"]
        )

    return render_template("display_foods.html", chef_foods=chef_foods, carts=cart)


@app.route("/customer_add_food", methods=["GET", "POST"])
@login_customer_required
def customer_add_food():
    """Insert Food Item into Database Table from Cart List """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if len(session["customer_cart"]) > 0:
            customer_id = session["user_id"]

            print("Before insert")
            db.execute(
                "INSERT INTO customer_order (customer_id,order_date) VALUES(?,current_timestamp)", customer_id)
            order_id = (db.execute("SELECT MAX(id) order_id FROM customer_order WHERE customer_id  = (?)", customer_id))[
                0].get("order_id")

            for x in session["customer_cart"]:
                chef_id = x.get("chef_id")
                food_name = x.get("food_name")
                price = x.get("price")

                db.execute("INSERT INTO customer_order_items (order_id,chef_id,item_description,price,delivery_status) VALUES(?,?,?,?,?)",
                           order_id, chef_id, food_name, price, 'Pending')

            session["customer_cart"] = []
            session["chef_foods"] = []

            return customer_info(" ", 200, "Your order is successfully placed! Order#: " + str(order_id))

        else:
            return customer_info(" ", 400, "Please add food item before placing Order!")

    else:

        # Redirect user to home page
        return redirect("/customer_home")


@app.route("/customer_view_order")
@login_customer_required
def customer_view_orders():
    """Show Customer Orders"""

    # Redirect user to home page
    return redirect("/customer_home")


@app.route("/register_chef", methods=["GET", "POST"])
def register_chef():
    """Register Chef"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        firstname = request.form.get("firstname", None)
        lastname = request.form.get("lastname", None)
        middlename = request.form.get("middlename", None)
        streetnumber = request.form.get("streetnumber", None)
        streetaddress = request.form.get("streetaddress", None)
        city = request.form.get("city", None)
        state = request.form.get("state", None)
        zipcode = request.form.get("zipcode", None)
        country = request.form.get("country", None)
        phonenumber = request.form.get("phonenumber", None)
        emailaddress = request.form.get("emailaddress", None)

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure password is re-confirmed
        elif not confirmation:
            return apology("must confirm password", 400)

        # Ensure password and re-confirmation is same
        elif password != confirmation:
            return apology("password confirmation failed!", 400)

        # Query customers database if username already exists
        rows = db.execute(
            "SELECT * FROM customers WHERE username = ?", username)

        # Ensure username does not exists
        if len(rows) != 0:
            return apology("username already exists", 400)

        # Query chefs database if username already exists
        rows = db.execute(
            "SELECT * FROM chefs WHERE username = ?", username)

        # Ensure username does not exists
        if len(rows) != 0:
            return apology("username already exists", 400)

        # Generate password hash
        password_hash = generate_password_hash(password)

        db.execute("INSERT INTO chefs (username,hash,first_name,last_name,middle_name,street_number,street_address,city,state,zip_code,country,phone_number,email_address,verified_status) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   username, password_hash, firstname, lastname, middlename, streetnumber, streetaddress, city, state, zipcode, country, phonenumber, emailaddress, 'NO')

        rows = db.execute(
            "SELECT id FROM chefs WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/chef_home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register_chef.html")


@app.route("/login_chef", methods=["GET", "POST"])
def login_chef():
    """Log Chef in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM chefs WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/chef_home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login_chef.html")


@app.route("/chef_home")
@login_chef_required
def chef_home():
    """Show Chefs Menu"""

    order_amount = 0

    menus = db.execute(
        "SELECT chefs.first_name || ' ' || chefs.middle_name || ' ' || chefs.last_name as chef_name,chef_menu.id,chef_menu.food_name,chef_menu.price,chef_menu.ingredients,chef_menu.register_date,chef_menu.meat_category FROM chef_menu INNER JOIN chefs ON (chef_menu.chef_id = chefs.id) WHERE chef_menu.chef_id = (?) ", session.get("user_id"))

    rows = db.execute(
        "SELECT sum(price) order_amount from chef_menu WHERE chef_id = (?) ", session.get("user_id"))

    if len(menus) > 0:
        order_amount = rows[0].get("order_amount")
    else:
        order_amount = 0

    return render_template("chef_home.html", menus=menus, order_total=order_amount)


@app.route("/chef_add_menu", methods=["GET", "POST"])
@login_chef_required
def chef_add_menu():

    # Ensure Cart exists

    if 'chef_cart_add' not in session:
        session["chef_cart_add"] = []

    if 'chef_cart_remove' in session:
        session["chef_cart_remove"] = []

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        chef_id = session.get("user_id")
        food_name = request.form.get("food_name")
        ingredients = request.form.get("ingredients")
        price = float(request.form.get("price"))
        meat_category = request.form.get("meat_category")
        print("Meat Category Here " + meat_category)

        if food_name:
            cart_id = len(session.get("chef_cart_add")) + 1
            food = {"cart_id": cart_id, "food_name": food_name,
                    "ingredients": ingredients, "price": price, "meat_category": meat_category}
            session["chef_cart_add"].append(food)

        return redirect("/chef_add_menu")

    # GET
    cart = session["chef_cart_add"]

    return render_template("chef_add_menu.html", carts=cart)


@app.route("/chef_remove_cart", methods=["GET", "POST"])
@login_chef_required
def chef_remove_cart():
    """Remove Item from Cart """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        cart_id = int(request.form.get("cart_id"))

        if cart_id:
            session["chef_cart_add"] = [
                x for x in session["chef_cart_add"] if (cart_id != x.get("cart_id"))]

        return redirect("/chef_remove_cart")

    # GET
    cart = session["chef_cart_add"]

    return render_template("chef_add_menu.html", carts=cart)


@app.route("/chef_insert_menu", methods=["GET", "POST"])
@login_chef_required
def chef_insert_menu():
    """Insert Food Item into Database Table "menu" from Cart List """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if len(session["chef_cart_add"]) > 0:
            chef_id = session["user_id"]

            for x in session["chef_cart_add"]:
                food_name = x.get("food_name")
                ingredients = x.get("ingredients")
                price = x.get("price")
                meat_category = x.get("meat_category")

                print("meat_category" + meat_category)

                db.execute("INSERT INTO chef_menu (chef_id,food_name,price,ingredients,meat_category,register_date) VALUES(?,?,?,?,?,current_timestamp)",
                           chef_id, food_name, price, ingredients, meat_category)

            session["chef_cart_add"] = []
            return chef_info("Your menu is successfully registered", 200)

        else:
            return chef_info("Please add a food item before registering food", 400)

    else:

        # Redirect user to home page
        return redirect("/chef_home")


@app.route("/chef_remove_menu", methods=["GET", "POST"])
@login_chef_required
def chef_remove_menu():

   # Ensure Cart exists
    if 'chef_cart_remove' not in session:
        session["chef_cart_remove"] = []

    if 'chef_cart_add' in session:
        session["chef_cart_add"] = []

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        menu_id = int(request.form.get("menu_id"))
        chef_id = int(request.form.get("chef_id"))
        food_name = request.form.get("food_name")
        ingredients = request.form.get("ingredients")
        meat_category = request.form.get("meat_category")
        price = float(request.form.get("price"))
        register_date = request.form.get("register_date")

        if menu_id:
            cart_id = len(session.get("chef_cart_remove")) + 1
            food = {"cart_id": cart_id, "id": menu_id, "chef_id": chef_id, "food_name": food_name,
                    "ingredients": ingredients, "price": price, "register_date": register_date, "meat_category": meat_category}
            session["chef_cart_remove"].append(food)

        return redirect("/chef_remove_menu")

    # GET
    cart = session["chef_cart_remove"]

    cart_id_list = [x.get("id") for x in cart]

    if len(cart_id_list) > 0:
        chef_menus = db.execute(
            "SELECT * FROM chef_menu where chef_id = (?) and id not in (?)", session["user_id"], cart_id_list
        )
    else:
        chef_menus = db.execute(
            "SELECT * FROM chef_menu where chef_id = (?) ", session["user_id"]
        )

    return render_template("chef_remove_menu.html", chef_menus=chef_menus, carts=cart)


@app.route("/chef_move_menu_from_cart", methods=["GET", "POST"])
@login_chef_required
def chef_move_menu_from_cart():

   # Ensure Cart exists
    if 'chef_cart_remove' not in session:
        session["chef_cart_remove"] = []

    if 'chef_cart_add' in session:
        session["chef_cart_add"] = []

        # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        cart_id = int(request.form.get("cart_id"))

        if cart_id:
            session["chef_cart_remove"] = [
                x for x in session["chef_cart_remove"] if (cart_id != x.get("cart_id"))]

        return redirect("/chef_move_menu_from_cart")

    # GET
    cart = session["chef_cart_remove"]

    cart_id_list = [x.get("id") for x in cart]

    if len(cart_id_list) > 0:
        chef_menus = db.execute(
            "SELECT * FROM chef_menu where chef_id = (?) and id not in (?)", session["user_id"], cart_id_list
        )
    else:
        chef_menus = db.execute(
            "SELECT * FROM chef_menu where chef_id = (?) ", session["user_id"]
        )

    return render_template("chef_remove_menu.html", chef_menus=chef_menus, carts=cart)


@app.route("/chef_deregister_menu", methods=["GET", "POST"])
@login_chef_required
def deregister_menu():

   # Ensure Cart exists
    if 'chef_cart_remove' not in session:
        session["chef_cart_remove"] = []

  # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        cart = session["chef_cart_remove"]

        cart_id_list = [x.get("id") for x in cart]

        if len(cart_id_list) > 0:
            db.execute(
                "DELETE FROM chef_menu where chef_id = (?) and id in (?)", session["user_id"], cart_id_list
            )

            session["chef_cart_remove"] = []
            return chef_info("Your menu is successfully Deregistered", 200)

        else:
            return chef_info("Please add food item to the cart before de-registering food!", 400)

    else:

        # Redirect user to home page
        return redirect("/chef_home")


@app.route("/chef_view_my_foods")
@login_chef_required
def chef_view_my_foods():
    """Show Chefs Registered Foods"""

    # Redirect user to home page
    return redirect("/chef_home")


@app.route("/chef_view_my_customer_orders")
@login_chef_required
def chef_view_my_customer_orders():
    """Show Chefs Assigned Food Order from Customer"""

    orders = db.execute(
        "SELECT customer_order.id as order_id,customer_order.order_date,item.id item_id,item.item_description,item.price,item.chef_id,concat(customers.first_name,' ',customers.last_name) as customer_name,item.delivery_status FROM customer_order INNER JOIN customer_order_items item ON ( customer_order.id = item.order_id ) INNER JOIN customers ON ( customer_order.customer_id = customers.id ) WHERE item.chef_id = (?) and delivery_status = 'Pending'", session.get("user_id"))

    rows = db.execute(
        "SELECT sum(item.price) order_amount FROM customer_order  INNER JOIN customer_order_items item ON ( customer_order.id = item.order_id ) INNER JOIN chefs ON ( item.chef_id = chefs.id ) WHERE item.chef_id = (?) and delivery_status = 'Pending'", session.get("user_id"))

    if len(orders) > 0:
        order_amount = rows[0].get("order_amount")
    else:
        order_amount = 0

    return render_template("chef_view_my_customer_orders.html", orders=orders, order_total=order_amount)


@app.route("/login_administrator", methods=["GET", "POST"])
def login_administrator():
    """Administrator Log in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure username should be administrator
        if request.form.get("username") != "administrator":
            return apology("username must be administrator", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM administrator WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/administrator_home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login_administrator.html")


@app.route("/administrator_home")
@login_administrator_required
def administrator_home():
    """Show Customer Orders"""

    customer_count = 0
    chef_count = 0

    customer_info = db.execute(
        "SELECT concat(customers.first_name,' ',customers.middle_name,' ',customers.last_name) as customer_name,concat(customers.street_number,' ',customers.street_address,' ',customers.city,' ',customers.zip_code,' ',customers.country) as address,customers.phone_number,customers.email_address FROM customers")

    chefs_info = db.execute(
        "SELECT concat(chefs.first_name,' ',chefs.middle_name,' ',chefs.last_name) as chef_name,concat(chefs.street_number,' ',chefs.street_address,' ',chefs.city,' ',chefs.zip_code,' ',chefs.country) as address,chefs.phone_number,chefs.email_address,chefs.verified_status FROM chefs")

    return render_template("administrator_home.html", customer_info=customer_info, chefs_info=chefs_info)


@app.route("/administrator_view_chef_menus")
@login_administrator_required
def administrator_view_chef_menus():
    """Show Menus from All Chefs """

    order_amount = 0

    menus = db.execute(
        "SELECT concat(chefs.first_name,' ',chefs.middle_name,' ',chefs.last_name) as chef_name,chef_menu.id,chef_menu.food_name,chef_menu.price,chef_menu.ingredients,chef_menu.register_date,chef_menu.meat_category FROM chef_menu INNER JOIN chefs ON (chef_menu.chef_id = chefs.id) ")

    rows = db.execute(
        "SELECT sum(price) order_amount FROM chef_menu ")

    if len(menus) > 0:
        order_amount = rows[0].get("order_amount")
    else:
        order_amount = 0

    return render_template("administrator_view_chef_menus.html", menus=menus, order_amount=order_amount)


@app.route("/administrator_view_customer_orders")
@login_administrator_required
def administrator_view_customer_orders():
    """Show Orders from All Customer"""

    order_total = 0
    orders = db.execute(
        "SELECT customer_order.id as order_id,customer_order.order_date,item.id item_id,item.item_description,item.price,item.chef_id,chefs.username as chef_name,item.delivery_status FROM customer_order  INNER JOIN customer_order_items item ON ( customer_order.id = item.order_id ) INNER JOIN chefs ON ( item.chef_id = chefs.id ) ")

    if len(orders) > 0:
        customer_count = 1
    else:
        customer_count = 0

    return render_template("administrator_view_customer_orders.html", orders=orders, customer_count=customer_count, order_total=order_total)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
