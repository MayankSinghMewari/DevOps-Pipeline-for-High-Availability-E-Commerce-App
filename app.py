# Streamlit E-commerce App with Proper Page Navigation

import streamlit as st
import pymongo
from bson import ObjectId
import hashlib

# Configure page
st.set_page_config(
    page_title="MyShop E-commerce",
    page_icon="🛍️",
    layout="wide"
)

# MongoDB Connection with error handling
@st.cache_resource
def init_connection():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["ecommerce_db"]
        # Test connection
        client.admin.command('ismaster')
        return db, True
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None, False

db, db_connected = init_connection()

# Initialize session state
if "cart" not in st.session_state:
    st.session_state.cart = []
if "user" not in st.session_state:
    st.session_state.user = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_to_cart(product_id):
    if product_id not in st.session_state.cart:
        st.session_state.cart.append(product_id)
        st.success("✅ Added to cart!")
    else:
        st.warning("Item already in cart!")

def remove_from_cart(product_id):
    if product_id in st.session_state.cart:
        st.session_state.cart.remove(product_id)
        st.success("Removed from cart!")

def clear_cart():
    st.session_state.cart = []

# Navigation
st.sidebar.title("🛍️ MyShop")

# User authentication section
if st.session_state.user is None:
    auth_option = st.sidebar.selectbox("Account", ["Login", "Register"])
    
    if auth_option == "Login":
        with st.sidebar.form("login_form"):
            st.subheader("Login")
            email = st.text_input("Email*")
            password = st.text_input("Password*", type="password")
            login_btn = st.form_submit_button("Login")
            
            if login_btn and email and password:
                if db_connected:
                    user = db.users.find_one({"email": email, "password": hash_password(password)})
                    if user:
                        st.session_state.user = user
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials!")
                else:
                    st.error("Database not available!")
    
    else:  # Register
        with st.sidebar.form("register_form"):
            st.subheader("Register")
            email = st.text_input("Email*")
            password = st.text_input("Password*", type="password")
            register_btn = st.form_submit_button("Register")
            
            if register_btn and email and password:
                if db_connected:
                    if db.users.find_one({"email": email}):
                        st.error("Email already exists!")
                    else:
                        db.users.insert_one({
                            "email": email,
                            "password": hash_password(password)
                        })
                        st.success("Registration successful! Please login.")
                else:
                    st.error("Database not available!")

else:
    st.sidebar.success(f"Welcome, {st.session_state.user['email']}!")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.cart = []
        st.rerun()

# Main navigation (only show if logged in)
if st.session_state.user:
    page = st.sidebar.selectbox(
        "Navigate", 
        ["Home", "Product Detail", "Cart", "Checkout"],
        index=["Home", "Product Detail", "Cart", "Checkout"].index(st.session_state.current_page)
    )
    st.session_state.current_page = page
    
    # Cart summary in sidebar
    cart_count = len(st.session_state.cart)
    st.sidebar.metric("Cart Items", cart_count)

else:
    page = "Login Required"

# -------------------------
# Pages
# -------------------------

if page == "Login Required":
    st.title("🛍️ Welcome to MyShop")
    st.info("Please login or register to access the store.")
    
    # Sample products preview (read-only)
    st.subheader("Featured Products")
    if db_connected:
        products = list(db.products.find().limit(3))
        if products:
            cols = st.columns(3)
            for i, product in enumerate(products):
                with cols[i]:
                    if 'image' in product:
                        st.image(product['image'], use_column_width=True)
                    st.write(f"**{product['name']}**")
                    st.write(f"₹{product['price']}")
        else:
            st.info("No products available. Make sure your database has sample products.")

elif page == "Home":
    st.title("🛍️ Product Catalog")
    
    if not db_connected:
        st.error("Database connection failed!")
        st.stop()
    
    # Search functionality
    search_term = st.text_input("🔍 Search products...")
    
    # Filter products based on search
    if search_term:
        products = list(db.products.find({
            "$or": [
                {"name": {"$regex": search_term, "$options": "i"}},
                {"description": {"$regex": search_term, "$options": "i"}}
            ]
        }))
    else:
        products = list(db.products.find())
    
    if not products:
        st.warning("No products found!")
        if st.button("Add Sample Products"):
            sample_products = [
                {"name": "Laptop", "price": 45000, "description": "High-performance laptop", "image": "https://via.placeholder.com/300x200"},
                {"name": "Smartphone", "price": 25000, "description": "Latest smartphone", "image": "https://via.placeholder.com/300x200"},
                {"name": "Headphones", "price": 3000, "description": "Wireless headphones", "image": "https://via.placeholder.com/300x200"}
            ]
            db.products.insert_many(sample_products)
            st.success("Sample products added! Refresh the page.")
    else:
        # Display products in a grid
        cols_per_row = 3
        for i in range(0, len(products), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, product in enumerate(products[i:i+cols_per_row]):
                with cols[j]:
                    # Product card
                    with st.container():
                        if 'image' in product:
                            st.image(product['image'], use_column_width=True)
                        st.subheader(product['name'])
                        st.write(f"**₹{product['price']}**")
                        st.write(product.get('description', 'No description'))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"View Details", key=f"detail_{product['_id']}"):
                                st.session_state.selected_product = str(product['_id'])
                                st.session_state.current_page = "Product Detail"
                                st.rerun()
                        with col2:
                            if st.button(f"Add to Cart", key=f"cart_{product['_id']}"):
                                add_to_cart(str(product['_id']))

elif page == "Product Detail":
    product_id = st.session_state.get('selected_product')
    
    if not product_id:
        st.warning("No product selected. Please go back to Home and select a product.")
        if st.button("← Back to Home"):
            st.session_state.current_page = "Home"
            st.rerun()
    else:
        try:
            product = db.products.find_one({"_id": ObjectId(product_id)})
            if product:
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    if 'image' in product:
                        st.image(product['image'], use_column_width=True)
                
                with col2:
                    st.title(product['name'])
                    st.subheader(f"₹{product['price']}")
                    st.write("**Description:**")
                    st.write(product.get("description", "No description available."))
                    
                    st.write("---")
                    
                    col_cart, col_amazon = st.columns(2)
                    with col_cart:
                        if st.button("🛒 Add to Cart", use_container_width=True):
                            add_to_cart(product_id)
                    
                    with col_amazon:
                        amazon_url = f"https://www.amazon.in/s?k={product['name'].replace(' ', '+')}"
                        st.link_button("Buy on Amazon", amazon_url, use_container_width=True)
                
                st.write("---")
                if st.button("← Back to Products"):
                    st.session_state.current_page = "Home"
                    st.rerun()
                    
            else:
                st.error("Product not found!")
                if st.button("← Back to Home"):
                    st.session_state.current_page = "Home"
                    st.rerun()
        except Exception as e:
            st.error(f"Error loading product: {e}")

elif page == "Cart":
    st.title("🛒 Your Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is empty.")
        if st.button("Continue Shopping"):
            st.session_state.current_page = "Home"
            st.rerun()
    else:
        try:
            cart_items = list(db.products.find({"_id": {"$in": [ObjectId(pid) for pid in st.session_state.cart]}}))
            total = 0
            
            # Display cart items
            for item in cart_items:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.write(f"**{item['name']}**")
                    st.write(item.get('description', '')[:50] + "...")
                
                with col2:
                    st.write(f"₹{item['price']}")
                
                with col3:
                    st.write("Qty: 1")
                
                with col4:
                    if st.button("Remove", key=f"remove_{item['_id']}"):
                        remove_from_cart(str(item['_id']))
                        st.rerun()
                
                total += item['price']
                st.divider()
            
            # Cart summary
            st.subheader(f"**Total: ₹{total}**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Continue Shopping"):
                    st.session_state.current_page = "Home"
                    st.rerun()
            with col2:
                if st.button("Clear Cart"):
                    clear_cart()
                    st.rerun()
            with col3:
                if st.button("Proceed to Checkout", type="primary"):
                    st.session_state.current_page = "Checkout"
                    st.rerun()
                    
        except Exception as e:
            st.error(f"Error loading cart: {e}")

elif page == "Checkout":
    st.title("💳 Checkout")
    
    if not st.session_state.cart:
        st.warning("Your cart is empty!")
        if st.button("Go to Home"):
            st.session_state.current_page = "Home"
            st.rerun()
    else:
        # Order summary
        cart_items = list(db.products.find({"_id": {"$in": [ObjectId(pid) for pid in st.session_state.cart]}}))
        total = sum(item['price'] for item in cart_items)
        
        st.subheader("Order Summary")
        for item in cart_items:
            st.write(f"• {item['name']} - ₹{item['price']}")
        
        st.subheader(f"**Total: ₹{total}**")
        st.write("---")
        
        # Checkout form
        with st.form("checkout_form"):
            st.subheader("Shipping Information")
            
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name*")
                phone = st.text_input("Phone Number*")
            with col2:
                last_name = st.text_input("Last Name*")
                email = st.text_input("Email*", value=st.session_state.user['email'], disabled=True)
            
            address = st.text_area("Address*")
            
            col1, col2 = st.columns(2)
            with col1:
                city = st.text_input("City*")
            with col2:
                pincode = st.text_input("Pincode*")
            
            st.subheader("Payment Method")
            payment_method = st.selectbox("Select Payment Method", ["Cash on Delivery", "Credit Card", "UPI"])
            
            place_order = st.form_submit_button("Place Order", type="primary")
            
            if place_order:
                if all([first_name, last_name, phone, address, city, pincode]):
                    if db_connected:
                        order = {
                            "user_id": st.session_state.user['_id'],
                            "user_email": st.session_state.user['email'],
                            "items": [str(pid) for pid in st.session_state.cart],
                            "total": total,
                            "shipping_info": {
                                "first_name": first_name,
                                "last_name": last_name,
                                "phone": phone,
                                "address": address,
                                "city": city,
                                "pincode": pincode
                            },
                            "payment_method": payment_method,
                            "status": "Confirmed"
                        }
                        db.orders.insert_one(order)
                    
                    st.success("🎉 Order placed successfully!")
                    st.balloons()
                    clear_cart()
                    
                    if st.button("Continue Shopping"):
                        st.session_state.current_page = "Home"
                        st.rerun()
                else:
                    st.error("Please fill all required fields!")
        
        if st.button("← Back to Cart"):
            st.session_state.current_page = "Cart"
            st.rerun()