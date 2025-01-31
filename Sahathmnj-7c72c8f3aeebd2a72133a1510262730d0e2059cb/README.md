# Personal Plates
#### Video Demo:  (https://www.youtube.com/watch?v=BtaIJJ5rRiw)
#### Description:

                The “Personal Plates” project is a web application created to give customers the satisfaction of home cooked meals, and homemakers the ability to make money and showcase their cooking skills. The user can choose to become a cook and make home cooked foods from the comfort of their own home, or be a customer, and order local meals from all types of cuisines. Each chef can decide what to cook, and the customers can look for foods near their location, and order delivery.

                This project is made using a flask framework. The main coding language is Python, using Jinja, with HTML and CSS being used to design and format the application by leveraging Bootstrap classes, and an SQLITE database to capture all of the data. The project has a static folder containing images and the css document, an app.py document, an SQLITE project database, and a templates folder, which has 24 HTML documents. The main page is created with the login.html document that extends the layout.html document. Both of these pages allow for the user to log in to the web application. There is also a chef’s layout and login page, and a customer’s layout and login page. The main page allows for both the chefs and the customers to log in. If it is the user’s first time on this application, then they can sign up by clicking the Customer Register button. If they want to work as a cook, then they can click the Register For Chef button. In the top right, there is an Administrator Login button for the creator to view all of the registered chefs and customers.

                To register as a chef, the chef’s register.html page is rendered, and the user has to provide their name, address, phone number, email address, preferred username, and chosen password. They are then checked by the admins to make sure they are credible. After, they are sent to the chef home page, which extends the chef’s layout page and is created by the chef home.html document. On this page, there are 6 buttons: Home, Add Foods, Remove Foods, View Registered Foods, View My Customer Orders, and Log Out. In the home page, made with the chef home.html document, the user can see the foods that they agreed to cook. If they are new, then they can add foods to their menu by clicking on the button. The Add Foods html document allows for the user to type in the name of their food they want to add to their menu, along with the ingredients, the price, and if it is vegan, vegetarian, or non vegetarian. The Remove Foods button allows for the user to remove foods from their menu. The View Registered Foods button shows the user their menu, and the View Customer Orders button lets the user see the most recent orders, which contain the order ID, food ID, food name, order date, delivery status, customer name, and the price.

                To register as a customer, the customer’s register.html page is rendered, and similar to the chef’s registration process, the user has to provide their name, address, phone number, email address, preferred username, and chosen password. Here, the user can click on the Home button, Place Order button, View Order button, or Log Out button. The Home button takes the user to the default page for the customer. The Place Order button allows the user to search for foods based on the name, zip code, meat category, and chef’s name. The user can then add their chosen food to the cart and place an order. They can then view their order by clicking on the corresponding button.

                Each type of user has specific methods and routes relating to them:



                For the customers,

                @app.route("/register_customer", methods=["GET", "POST"]) is for users that want to register as a customer. In the SQLITE database, there is a table created called customers that generates a unique ID for the user, and captures all the relevant information such as the user’s full address, phone number, and email address.

                @app.route("/login_customer", methods=["GET", "POST"]) is for users that already have an account.

                @app.route("/customer_home") takes the user to the default customer page if the login/registration is successful.

                @app.route("/customer_place_order", methods=["GET", "POST"]) is for users to place an order. It takes them to a search page where they can search for food based on the food name, zip code, meat category, or chef’s first name. If a search is found, this method will display the available foods with its price.

                @app.route("/customer_add_cart", methods=["GET", "POST"]) allows the user to add the food to the cart.

                @app.route("/customer_remove_cart", methods=["GET", "POST"]) allows the user to remove the food from the cart.

                @app.route("/customer_add_food", methods=["GET", "POST"]) places the user’s order into two tables. The customer_order table generates an order ID and inserts the order date, and the customer_order_items table has all of the food in the order. This table is linked to the “customer_order” table by the “order_id”.

                @app.route("/customer_view_order") is a menu option available for the user to view their order.



                For the cooks,

                @app.route("/register_chef", methods=["GET", "POST"]) is for users that want to register as a Chef and register their menu item for prospective customers to choose from. Similar to customer registration, the user needs to provide all the relevant details for successful registration. A chef's table is created, and it generates a unique ID for the user, and captures the user’s full name, address, phone number, and email address.

                @app.route("/login_chef", methods=["GET", "POST"]) is for users that have previously registered to be a chef.

                @app.route("/chef_home") takes the user to the default chef page upon successful login.

                @app.route("/chef_add_menu", methods=["GET", "POST"]) is provided to the user to register foods onto their menu. The menu items are stacked into the cart before confirmation.

                @app.route("/chef_insert_menu", methods=["GET", "POST"]) confirms the user’s menu. A table is produced called chef menu, and it generates an ID that is assigned to every food item registered. The chef’s ID in this table is linked to the ID in the chef’s table.

                @app.route("/chef_remove_cart", methods=["GET", "POST"]) can remove the chosen foods from the user’s menu. The removed food item will initially be moved to the cart before the final confirmation.

                @app.route("/chef_move_menu_from_cart", methods=["GET", "POST"]) removes the food from the cart, and puts it back into the menu.

                @app.route("/chef_deregister_menu", methods=["GET", "POST"]) is for the user to confirm the deregistration of the foods in their cart, and all of the items in the cart gets removed from the back end “chef menu” table.

                @app.route("/chef_view_my_foods") allows the user to see all of the registered items in their menu.

                @app.route("/chef_view_my_customer_orders") lets the user view their customer orders and if the order is “Pending” or “Delivered”, along with the order ID, food ID, food name, order date, customer name, and price.



                For the administrator,

                @app.route("/login_administrator", methods=["GET", "POST"]) is specific to the administrator, who can view all the registered chefs, customers, and customer orders.

                @app.route("/administrator_view_chef_menus") is available for the administrator to view all the registered chef food items.

                @app.route("/administrator_view_customer_orders") is available for the administrator to view all the customers current and past orders.



                For All Users,
                @app.route("/") sends the user to the main page, regardless if they are a customer or cook, where they can log in.

                @app.route("/logout") signs the user out of the website, and takes them to the default login page.
