# Project 3 - Pizza

A Web application for handling a pizza restaurant's online orders.

## Features
- Allow users to :
    - browse the restaurant's menu
    - add items to their cart
    - submit their orders
    - see the status of their orders (personal touch)
- Allow restaurant's owners to:
    - add and update menu
    - view customers' orders
    - update orders' status (personal touch)

## Orders app

### Database structure in orders/models.py
I use three classes to represent the restaurant's menu:

#### 1. Product
- Represent all six categories including: Regular Pizza, Sicilian Pizza, Subs, Pasta, Salad,  Dinner Platter

#### 2. ProductVariant
- Each product variant contains information about its called name (eg: special, 1 topping ... for pizza or veggie, steak... for sub), its price corresponding to its size, the number of toppings, and a boolean value if it is an addon variant or not

#### 3. Topping
- Represent all the toppings for pizza

I use two classes to represent orders coming from customers:
#### 1. Order:
Including fields that represent:
- User that placed this order
- Date that the order has been placed
- Status about the order: Received, Pendding or Done
- Total price (defined by function get_total)
- A list of items (defined by function get_items)

#### 2. OrderItem
Including field that represent:
- All the information the ProductVariant that it's linked to has: name, size, price...
- Quantity
- A list of toppings
- A list of addons
- Final unit price if the item has addons (defined by function get_unit_price)

### views.py
#### index + index.html
- Render the restaurant's menu and allowing users to add items to their shopping cart

#### add_to_cart
- Handle requests to add items to cart

#### update_item_quantity
- Handle requests to update items' quantity

#### delete_cart
- Handle requests to remove items from cart

#### get_cart + cart.html
- Render cart.html to display all the cart information including: item name, size, quantity, toppings (if any), addons (if any), unit price and total price. Users can also admend quantity of items, or delete items from cart before placing orders

#### place_order
- Handle requests to place orders:
    - save the orders to database
    - delete the original cart
    - redirect users to order.html render by the below function

#### order_summary + order.html

#### order_history + history. html
- Render history.html where users can view the orders information and their status updated by the restaurant's owner

### admin.py
- Beside customing the inline view for ProductAd and Order, I defined two actions "make_pendding" and "make_done", so that the restaurant's owner can 'bulkly' update the status of orders.

### main.js
- line 10-26: Disable the place-order-button by default
- line 28-61: Show modal (where users can add toppings, addons and add the item to cart) when any price-button is clicked
- line 64-89: Validate number of chosen toppings then get a list of them if they're valid
- line 91-101: Get a list of addons for subs
- line 103-119: Define function getCookie and call it to get csrf token which is used whenever submitting data to server via ajax post request.
- line 121-143: add items to cart
- line 145-190: Update item quantity in cart view
- line 192-208: Delete items from cart


## Users app
- I took advantage of the LoginView and LogoutView class from django.contrib.auth to log in and logout users.
- As the built-in UserCreationForm has three fields: username, password1, and password2 by default, I customed another form in users/forms.py called UserRegisterForm which has six fields username, first name, last name, email, password1, and password2.
- The urls for login, logout, register views are specified in project-level urls.py.




