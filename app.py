import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from dataclasses import dataclass
from typing import List, Dict
import numpy as np

# Configure page
st.set_page_config(
    page_title="Smart Grocery & Budget Assistant",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful background and styling
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Alternative grocery-themed background */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        opacity: 0.1;
        z-index: -1;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Main content area */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem;
    }
    
    /* Metric cards styling */
    .metric-container {
        background: linear-gradient(145deg, #ffffff, #f0f2f6);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #f8f9fa, #e9ecef);
        border-radius: 8px;
        border: 1px solid #dee2e6;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.5rem 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Form styling */
    .stForm {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    /* Headers styling */
    h1, h2, h3 {
        color: #2c3e50;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: linear-gradient(90deg, #d4edda, #c3e6cb);
        border-radius: 10px;
        border-left: 4px solid #28a745;
    }
    
    .stError {
        background: linear-gradient(90deg, #f8d7da, #f5c6cb);
        border-radius: 10px;
        border-left: 4px solid #dc3545;
    }
    
    .stWarning {
        background: linear-gradient(90deg, #fff3cd, #ffeaa7);
        border-radius: 10px;
        border-left: 4px solid #ffc107;
    }
    
    .stInfo {
        background: linear-gradient(90deg, #d1ecf1, #bee5eb);
        border-radius: 10px;
        border-left: 4px solid #17a2b8;
    }
    
    /* Plotly chart container */
    .js-plotly-plot {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Data frame styling */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #e9ecef;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.25);
    }
    
    /* Custom grocery background pattern */
    .grocery-pattern {
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
        background-size: 100px 100px;
    }
</style>
""", unsafe_allow_html=True)

# Data models
@dataclass
class GroceryItem:
    name: str
    category: str
    price: float
    quantity: int
    unit: str
    date_added: str
    expiry_date: str = None
    brand: str = None

@dataclass
class BudgetEntry:
    category: str
    allocated_amount: float
    spent_amount: float
    month: str

# Data persistence functions
def load_data():
    """Load data from JSON files"""
    grocery_data = []
    budget_data = []
    
    if os.path.exists('grocery_data.json'):
        with open('grocery_data.json', 'r') as f:
            grocery_data = json.load(f)
    
    if os.path.exists('budget_data.json'):
        with open('budget_data.json', 'r') as f:
            budget_data = json.load(f)
    
    return grocery_data, budget_data

def save_data(grocery_data, budget_data):
    """Save data to JSON files"""
    with open('grocery_data.json', 'w') as f:
        json.dump(grocery_data, f)
    
    with open('budget_data.json', 'w') as f:
        json.dump(budget_data, f)

# Initialize session state
if 'grocery_items' not in st.session_state:
    grocery_data, budget_data = load_data()
    st.session_state.grocery_items = grocery_data
    st.session_state.budget_entries = budget_data

# Authentication functions
def hash_password(password):
    """Simple password hashing (in production, use proper hashing like bcrypt)"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verify password against hashed password"""
    return hash_password(password) == hashed_password

def load_users():
    """Load user data from JSON file"""
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save user data to JSON file"""
    with open('users.json', 'w') as f:
        json.dump(users, f)

def forgot_password_page():
    """Display forgot password page"""
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 3rem;
        border-radius: 20px;
        margin: 2rem auto;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        max-width: 500px;
    ">
        <h1 style="
            color: #2c3e50;
            margin: 0 0 1rem 0;
            font-size: 2.5rem;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
        ">🔑 Forgot Password</h1>
        <p style="
            color: #2c3e50;
            margin: 0;
            font-size: 1.1rem;
            opacity: 0.8;
        ">Enter your username and email to reset your password</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Forgot password form
    with st.form("forgot_password_form"):
        st.markdown("### 🔐 Password Recovery")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("👤 Username", placeholder="Enter your username")
            email = st.text_input("📧 Email", placeholder="Enter your email address")
            
            recovery_col1, recovery_col2 = st.columns(2)
            with recovery_col1:
                verify_clicked = st.form_submit_button("🔍 Verify Account", type="primary")
            with recovery_col2:
                back_clicked = st.form_submit_button("⬅️ Back to Login")
    
    if verify_clicked:
        if username and email:
            users = load_users()
            
            if username in users and users[username]['email'] == email:
                st.session_state.reset_username = username
                st.session_state.show_reset_form = True
                st.success("✅ Account verified! You can now reset your password.")
                st.rerun()
            else:
                st.error("❌ Username and email combination not found!")
        else:
            st.error("⚠️ Please fill in all fields!")
    
    if back_clicked:
        st.session_state.show_forgot_password = False
        st.rerun()

def verify_and_reset_password():
    """Display password reset form after verification"""
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 3rem;
        border-radius: 20px;
        margin: 2rem auto;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        max-width: 500px;
    ">
        <h1 style="
            color: #2c3e50;
            margin: 0 0 1rem 0;
            font-size: 2.5rem;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
        ">🔄 Reset Password</h1>
        <p style="
            color: #2c3e50;
            margin: 0;
            font-size: 1.1rem;
            opacity: 0.8;
        ">Enter your new password</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Password reset form
    with st.form("reset_password_form"):
        st.markdown("### 🔑 Set New Password")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            new_password = st.text_input("🔑 New Password", type="password", placeholder="Enter new password")
            confirm_new_password = st.text_input("🔑 Confirm Password", type="password", placeholder="Confirm new password")
            
            reset_col1, reset_col2 = st.columns(2)
            with reset_col1:
                reset_clicked = st.form_submit_button("✅ Reset Password", type="primary")
            with reset_col2:
                cancel_clicked = st.form_submit_button("❌ Cancel")
    
    if reset_clicked:
        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                st.error("❌ Passwords don't match!")
            else:
                users = load_users()
                username = st.session_state.reset_username
                
                # Update password
                users[username]['password'] = hash_password(new_password)
                save_users(users)
                
                st.success("🎉 Password reset successfully!")
                st.info("👆 You can now login with your new password!")
                
                # Clear reset session state
                st.session_state.reset_username = None
                st.session_state.show_reset_form = False
                st.session_state.show_forgot_password = False
                st.rerun()
        else:
            st.error("⚠️ Please fill in all fields!")
    
    if cancel_clicked:
        st.session_state.reset_username = None
        st.session_state.show_reset_form = False
        st.session_state.show_forgot_password = False
        st.rerun()

def load_user_data(username):
    """Load specific user's grocery and budget data"""
    grocery_file = f'{username}_grocery_data.json'
    budget_file = f'{username}_budget_data.json'
    
    grocery_data = []
    budget_data = []
    
    if os.path.exists(grocery_file):
        with open(grocery_file, 'r') as f:
            grocery_data = json.load(f)
    
    if os.path.exists(budget_file):
        with open(budget_file, 'r') as f:
            budget_data = json.load(f)
    
    return grocery_data, budget_data

def save_user_data(username, grocery_data, budget_data):
    """Save specific user's grocery and budget data"""
    grocery_file = f'{username}_grocery_data.json'
    budget_file = f'{username}_budget_data.json'
    
    with open(grocery_file, 'w') as f:
        json.dump(grocery_data, f)
    
    with open(budget_file, 'w') as f:
        json.dump(budget_data, f)

def login_page():
    """Display login page"""
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 20px;
        margin: 2rem auto;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        max-width: 500px;
    ">
        <h1 style="
            color: white;
            margin: 0 0 1rem 0;
            font-size: 2.5rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        ">🛒 Welcome Back!</h1>
        <p style="
            color: rgba(255, 255, 255, 0.9);
            margin: 0;
            font-size: 1.1rem;
        ">Sign in to access your grocery data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    with st.form("login_form"):
        st.markdown("### 🔐 Login to Your Account")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
            
            login_col1, login_col2 = st.columns(2)
            with login_col1:
                login_clicked = st.form_submit_button("🚀 Login", type="primary")
            with login_col2:
                signup_clicked = st.form_submit_button("📝 Sign Up")
            
            # Forgot password link
            st.markdown("---")
            forgot_password_clicked = st.form_submit_button("🔑 Forgot Password?")
    
    if login_clicked:
        if username and password:
            users = load_users()
            
            if username in users and verify_password(password, users[username]['password']):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_email = users[username]['email']
                
                # Load user's data
                grocery_data, budget_data = load_user_data(username)
                st.session_state.grocery_items = grocery_data
                st.session_state.budget_entries = budget_data
                
                st.success(f"🎉 Welcome back, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password!")
        else:
            st.error("⚠️ Please fill in all fields!")
    
    if signup_clicked:
        st.session_state.show_signup = True
        st.rerun()
    
    if forgot_password_clicked:
        st.session_state.show_forgot_password = True
        st.rerun()

def forgot_password_page():
    """Display forgot password page"""
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 3rem;
        border-radius: 20px;
        margin: 2rem auto;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        max-width: 500px;
    ">
        <h1 style="
            color: #2c3e50;
            margin: 0 0 1rem 0;
            font-size: 2.5rem;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
        ">🔐 Reset Password</h1>
        <p style="
            color: #2c3e50;
            margin: 0;
            font-size: 1.1rem;
            opacity: 0.8;
        ">Enter your details to reset your password</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we're in the verification step
    if st.session_state.get('forgot_password_step') == 'verify':
        verify_and_reset_password()
        return
    
    # Password reset request form
    with st.form("forgot_password_form"):
        st.markdown("### 🔑 Password Reset Request")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("👤 Username", placeholder="Enter your username")
            email = st.text_input("📧 Email", placeholder="Enter your email address")
            
            reset_col1, reset_col2 = st.columns(2)
            with reset_col1:
                request_reset_clicked = st.form_submit_button("🔄 Request Reset", type="primary")
            with reset_col2:
                back_clicked = st.form_submit_button("⬅️ Back to Login")
    
    if request_reset_clicked:
        if username and email:
            users = load_users()
            
            if username in users and users[username]['email'] == email:
                # Store the username for the next step
                st.session_state.reset_username = username
                st.session_state.forgot_password_step = 'verify'
                st.success("✅ User verified! Please answer the security question.")
                st.rerun()
            else:
                st.error("❌ Username and email combination not found!")
        else:
            st.error("⚠️ Please fill in all fields!")
    
    if back_clicked:
        st.session_state.show_forgot_password = False
        st.rerun()

def verify_and_reset_password():
    """Verify security question and allow password reset"""
    st.markdown("### 🛡️ Security Verification")
    
    # Simple security questions (in a real app, you'd store the user's chosen question and answer)
    security_questions = [
        "What was the name of your first pet?",
        "What city were you born in?",
        "What is your mother's maiden name?",
        "What was your first car model?",
        "What is your favorite food?"
    ]
    
    with st.form("verify_reset_form"):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info(f"🔐 Resetting password for: **{st.session_state.reset_username}**")
            
            # For demo purposes, we'll use a simple security question
            # In a real app, you'd retrieve the user's chosen question and verify their answer
            selected_question = st.selectbox("🤔 Security Question", security_questions)
            security_answer = st.text_input("✍️ Your Answer", placeholder="Enter your answer")
            
            st.markdown("---")
            st.markdown("**🔑 Set New Password**")
            new_password = st.text_input("🔒 New Password", type="password", placeholder="Enter new password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm new password")
            
            verify_col1, verify_col2 = st.columns(2)
            with verify_col1:
                reset_clicked = st.form_submit_button("✅ Reset Password", type="primary")
            with verify_col2:
                cancel_clicked = st.form_submit_button("❌ Cancel")
    
    if reset_clicked:
        if security_answer and new_password and confirm_password:
            if new_password != confirm_password:
                st.error("❌ Passwords don't match!")
            elif len(new_password) < 6:
                st.error("❌ Password must be at least 6 characters long!")
            else:
                # For demo purposes, accept any non-empty security answer
                # In a real app, you'd verify against the stored answer
                users = load_users()
                username = st.session_state.reset_username
                
                # Update the password
                users[username]['password'] = hash_password(new_password)
                users[username]['password_reset_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_users(users)
                
                st.success(f"🎉 Password reset successfully for {username}!")
                st.info("👆 You can now login with your new password!")
                
                # Clear the session state
                st.session_state.forgot_password_step = None
                st.session_state.reset_username = None
                st.session_state.show_forgot_password = False
                st.rerun()
        else:
            st.error("⚠️ Please fill in all fields!")
    
    if cancel_clicked:
        st.session_state.forgot_password_step = None
        st.session_state.reset_username = None
        st.session_state.show_forgot_password = False
        st.rerun()

def signup_page():
    """Display signup page"""
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 3rem;
        border-radius: 20px;
        margin: 2rem auto;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        max-width: 500px;
    ">
        <h1 style="
            color: #2c3e50;
            margin: 0 0 1rem 0;
            font-size: 2.5rem;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
        ">🌟 Join Us!</h1>
        <p style="
            color: #2c3e50;
            margin: 0;
            font-size: 1.1rem;
            opacity: 0.8;
        ">Create your account and start smart shopping</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Signup form
    with st.form("signup_form"):
        st.markdown("### 📝 Create New Account")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            new_username = st.text_input("👤 Username", placeholder="Choose a username")
            email = st.text_input("📧 Email", placeholder="Enter your email")
            new_password = st.text_input("🔑 Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("🔑 Confirm Password", type="password", placeholder="Confirm your password")
            
            signup_col1, signup_col2 = st.columns(2)
            with signup_col1:
                create_clicked = st.form_submit_button("✨ Create Account", type="primary")
            with signup_col2:
                back_clicked = st.form_submit_button("⬅️ Back to Login")
    
    if create_clicked:
        if new_username and email and new_password and confirm_password:
            if new_password != confirm_password:
                st.error("❌ Passwords don't match!")
            else:
                users = load_users()
                
                if new_username in users:
                    st.error("❌ Username already exists!")
                else:
                    # Create new user
                    users[new_username] = {
                        'password': hash_password(new_password),
                        'email': email,
                        'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    save_users(users)
                    
                    # Initialize empty data for new user
                    save_user_data(new_username, [], [])
                    
                    st.success(f"🎉 Account created successfully for {new_username}!")
                    st.info("👆 You can now login with your credentials!")
                    st.session_state.show_signup = False
                    st.rerun()
        else:
            st.error("⚠️ Please fill in all fields!")
    
    if back_clicked:
        st.session_state.show_signup = False
        st.rerun()

# Initialize authentication session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False
if 'show_forgot_password' not in st.session_state:
    st.session_state.show_forgot_password = False
if 'show_reset_form' not in st.session_state:
    st.session_state.show_reset_form = False
if 'reset_username' not in st.session_state:
    st.session_state.reset_username = None

# Helper functions
def get_category_suggestions():
    return [
        "🥬 Fruits & Vegetables", "🥛 Dairy & Eggs", "🥩 Meat & Seafood", 
        "🍞 Bakery", "🥫 Pantry Staples", "🥤 Beverages", "🍿 Snacks",
        "🧊 Frozen Foods", "🧴 Personal Care", "🧽 Household Items",
        "👶 Baby Products", "🐕 Pet Supplies"
    ]

def get_category_emoji(category):
    """Get emoji for category"""
    emoji_map = {
        "🥬 Fruits & Vegetables": "🥬", "Fruits & Vegetables": "🥬",
        "🥛 Dairy & Eggs": "🥛", "Dairy & Eggs": "🥛",
        "🥩 Meat & Seafood": "🥩", "Meat & Seafood": "🥩",
        "🍞 Bakery": "🍞", "Bakery": "🍞",
        "🥫 Pantry Staples": "🥫", "Pantry Staples": "🥫",
        "🥤 Beverages": "🥤", "Beverages": "🥤",
        "🍿 Snacks": "🍿", "Snacks": "🍿",
        "🧊 Frozen Foods": "🧊", "Frozen Foods": "🧊",
        "🧴 Personal Care": "🧴", "Personal Care": "🧴",
        "🧽 Household Items": "🧽", "Household Items": "🧽",
        "👶 Baby Products": "👶", "Baby Products": "👶",
        "🐕 Pet Supplies": "🐕", "Pet Supplies": "🐕"
    }
    return emoji_map.get(category, "🛒")

def get_item_emoji(item_name):
    """Get emoji for specific grocery items"""
    item_name_lower = item_name.lower()
    
    # Fruits & Vegetables
    if any(fruit in item_name_lower for fruit in ['apple', 'apples']):
        return "🍎"
    elif any(fruit in item_name_lower for fruit in ['banana', 'bananas']):
        return "🍌"
    elif 'avocado' in item_name_lower:
        return "🥑"
    elif any(veg in item_name_lower for veg in ['onion', 'onions']):
        return "🧅"
    elif any(veg in item_name_lower for veg in ['carrot', 'carrots']):
        return "🥕"
    elif any(veg in item_name_lower for veg in ['tomato', 'tomatoes']):
        return "🍅"
    elif any(veg in item_name_lower for veg in ['potato', 'potatoes']):
        return "🥔"
    elif any(veg in item_name_lower for veg in ['lettuce', 'salad', 'greens']):
        return "🥬"
    elif any(fruit in item_name_lower for fruit in ['orange', 'oranges']):
        return "🍊"
    elif any(fruit in item_name_lower for fruit in ['lemon', 'lemons']):
        return "🍋"
    elif any(fruit in item_name_lower for fruit in ['strawberry', 'strawberries']):
        return "🍓"
    elif any(fruit in item_name_lower for fruit in ['grape', 'grapes']):
        return "🍇"
    elif any(veg in item_name_lower for veg in ['pepper', 'bell pepper']):
        return "🫑"
    elif any(veg in item_name_lower for veg in ['broccoli']):
        return "🥦"
    elif any(veg in item_name_lower for veg in ['cucumber']):
        return "🥒"
    
    # Dairy & Eggs
    elif any(dairy in item_name_lower for dairy in ['milk', 'dairy']):
        return "🥛"
    elif any(dairy in item_name_lower for dairy in ['cheese', 'cheddar', 'mozzarella']):
        return "🧀"
    elif any(dairy in item_name_lower for dairy in ['egg', 'eggs']):
        return "🥚"
    elif any(dairy in item_name_lower for dairy in ['butter']):
        return "🧈"
    elif any(dairy in item_name_lower for dairy in ['yogurt', 'yoghurt']):
        return "🥛"
    
    # Meat & Seafood
    elif any(meat in item_name_lower for meat in ['chicken', 'poultry']):
        return "🍗"
    elif any(meat in item_name_lower for meat in ['beef', 'steak']):
        return "🥩"
    elif any(meat in item_name_lower for meat in ['pork', 'ham', 'bacon']):
        return "🥓"
    elif any(fish in item_name_lower for fish in ['fish', 'salmon', 'tuna']):
        return "🐟"
    elif any(seafood in item_name_lower for seafood in ['shrimp', 'prawns']):
        return "🦐"
    
    # Bakery
    elif any(bread in item_name_lower for bread in ['bread', 'loaf']):
        return "🍞"
    elif any(baked in item_name_lower for baked in ['croissant']):
        return "🥐"
    elif any(baked in item_name_lower for baked in ['bagel']):
        return "🥯"
    elif any(baked in item_name_lower for baked in ['cake', 'muffin']):
        return "🧁"
    
    # Beverages
    elif any(drink in item_name_lower for drink in ['coffee', 'espresso']):
        return "☕"
    elif any(drink in item_name_lower for drink in ['tea']):
        return "🍵"
    elif any(drink in item_name_lower for drink in ['juice', 'orange juice']):
        return "🧃"
    elif any(drink in item_name_lower for drink in ['water', 'bottle']):
        return "💧"
    elif any(drink in item_name_lower for drink in ['beer']):
        return "🍺"
    elif any(drink in item_name_lower for drink in ['wine']):
        return "🍷"
    elif any(drink in item_name_lower for drink in ['soda', 'cola', 'soft drink']):
        return "🥤"
    
    # Pantry Staples
    elif any(staple in item_name_lower for staple in ['rice']):
        return "🍚"
    elif any(staple in item_name_lower for staple in ['pasta', 'spaghetti']):
        return "🍝"
    elif any(staple in item_name_lower for staple in ['oil', 'olive oil']):
        return "🫒"
    elif any(staple in item_name_lower for staple in ['salt']):
        return "🧂"
    elif any(staple in item_name_lower for staple in ['honey']):
        return "🍯"
    
    # Snacks
    elif any(snack in item_name_lower for snack in ['chips', 'crisps']):
        return "🍟"
    elif any(snack in item_name_lower for snack in ['chocolate', 'candy']):
        return "🍫"
    elif any(snack in item_name_lower for snack in ['cookie', 'biscuit']):
        return "🍪"
    elif any(snack in item_name_lower for snack in ['popcorn']):
        return "🍿"
    elif any(snack in item_name_lower for snack in ['nuts', 'almonds', 'peanuts']):
        return "🥜"
    
    # Default emoji based on category
    else:
        return "🛒"

def calculate_total_spent():
    """Calculate total amount spent"""
    total = sum(item['price'] * item['quantity'] for item in st.session_state.grocery_items)
    return total

def get_spending_by_category():
    """Get spending breakdown by category"""
    category_spending = {}
    for item in st.session_state.grocery_items:
        category = item['category']
        amount = item['price'] * item['quantity']
        category_spending[category] = category_spending.get(category, 0) + amount
    return category_spending

def get_budget_vs_actual():
    """Compare budget vs actual spending"""
    category_spending = get_spending_by_category()
    current_month = datetime.now().strftime("%Y-%m")
    
    budget_comparison = []
    for entry in st.session_state.budget_entries:
        if entry['month'] == current_month:
            actual_spent = category_spending.get(entry['category'], 0)
            budget_comparison.append({
                'category': entry['category'],
                'budgeted': entry['allocated_amount'],
                'actual': actual_spent,
                'remaining': entry['allocated_amount'] - actual_spent
            })
    
    return budget_comparison

# Main app
def main():
    # Check if user is logged in
    if not st.session_state.logged_in:
        if st.session_state.get('show_signup', False):
            signup_page()
        elif st.session_state.get('show_forgot_password', False):
            if st.session_state.get('show_reset_form', False):
                verify_and_reset_password()
            else:
                forgot_password_page()
        else:
            login_page()
        return
    
    # Beautiful header with gradient background and user info
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    ">
        <h1 style="
            color: white;
            margin: 0;
            font-size: 3rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        ">🛒 Smart Grocery & Budget Assistant</h1>
        <p style="
            color: rgba(255, 255, 255, 0.9);
            margin: 0.5rem 0 0 0;
            font-size: 1.2rem;
        ">Track • Budget • Save • Smart Shopping Made Easy</p>
        <p style="
            color: rgba(255, 255, 255, 0.8);
            margin: 0.5rem 0 0 0;
            font-size: 1rem;
        ">👤 Welcome, {st.session_state.username}!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation with logout
    st.sidebar.title("🧭 Navigation")
    
    # User info in sidebar
    st.sidebar.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    ">
        <h4 style="margin: 0; color: #2c3e50;">👤 {st.session_state.username}</h4>
        <p style="margin: 0; color: #2c3e50; font-size: 0.8rem; opacity: 0.7;">{st.session_state.user_email}</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["📊 Dashboard", "➕ Add Grocery Item", "📝 Grocery List", "💰 Budget Manager", "📈 Analytics", "🎯 Smart Recommendations"]
    )
    
    # Logout button
    if st.sidebar.button("🚪 Logout", type="secondary"):
        # Save current user data before logout
        save_user_data(st.session_state.username, st.session_state.grocery_items, st.session_state.budget_entries)
        
        # Clear session state
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_email = None
        st.session_state.grocery_items = []
        st.session_state.budget_entries = []
        st.rerun()
    
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "➕ Add Grocery Item":
        add_grocery_item()
    elif page == "📝 Grocery List":
        show_grocery_list()
    elif page == "💰 Budget Manager":
        budget_manager()
    elif page == "📈 Analytics":
        show_analytics()
    elif page == "🎯 Smart Recommendations":
        show_recommendations()

def show_dashboard():
    st.markdown('<div class="grocery-pattern">', unsafe_allow_html=True)
    
    # Beautiful section header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.1);
    ">
        <h2 style="color: white; margin: 0; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);">📊 Your Grocery Dashboard</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics with beautiful cards
    col1, col2, col3, col4 = st.columns(4)
    
    total_items = len(st.session_state.grocery_items)
    total_spent = calculate_total_spent()
    category_count = len(set(item['category'] for item in st.session_state.grocery_items))
    
    with col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 6px 25px rgba(102, 126, 234, 0.3);
            transform: translateY(0);
            transition: transform 0.3s ease;
        ">
            <h3 style="margin: 0; font-size: 2.5rem;">🛍️</h3>
            <h2 style="margin: 0.5rem 0; font-size: 2rem;">{total_items}</h2>
            <p style="margin: 0; opacity: 0.9;">Total Items</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            color: #2c3e50;
            box-shadow: 0 6px 25px rgba(252, 182, 159, 0.3);
        ">
            <h3 style="margin: 0; font-size: 2.5rem;">💰</h3>
            <h2 style="margin: 0.5rem 0; font-size: 2rem;">€{total_spent:.2f}</h2>
            <p style="margin: 0; opacity: 0.8;">Total Spent</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            color: #2c3e50;
            box-shadow: 0 6px 25px rgba(168, 237, 234, 0.3);
        ">
            <h3 style="margin: 0; font-size: 2.5rem;">📂</h3>
            <h2 style="margin: 0.5rem 0; font-size: 2rem;">{category_count}</h2>
            <p style="margin: 0; opacity: 0.8;">Categories</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_item_cost = total_spent / total_items if total_items > 0 else 0
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            color: #2c3e50;
            box-shadow: 0 6px 25px rgba(210, 153, 194, 0.3);
        ">
            <h3 style="margin: 0; font-size: 2.5rem;">📊</h3>
            <h2 style="margin: 0.5rem 0; font-size: 2rem;">€{avg_item_cost:.2f}</h2>
            <p style="margin: 0; opacity: 0.8;">Avg Item Cost</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent purchases
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 12px;
        margin: 2rem 0 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="color: #2c3e50; margin: 0;">🛒 Recent Purchases</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.grocery_items:
        recent_items = sorted(
            st.session_state.grocery_items,
            key=lambda x: x['date_added'],
            reverse=True
        )[:5]
        
        for item in recent_items:
            item_emoji = get_item_emoji(item['name'])
            with st.expander(f"{item_emoji} {item['name']} - €{item['price']:.2f}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    category_emoji = get_category_emoji(item['category'])
                    st.write(f"**Category:** {category_emoji} {item['category']}")
                with col2:
                    st.write(f"**Quantity:** {item['quantity']} {item['unit']}")
                with col3:
                    st.write(f"**Date:** {item['date_added']}")
    else:
        st.info("No grocery items added yet. Start by adding some items!")
    
    # Quick budget overview
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 12px;
        margin: 2rem 0 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="color: #2c3e50; margin: 0;">💰 Budget Overview</h3>
    </div>
    """, unsafe_allow_html=True)
    budget_comparison = get_budget_vs_actual()
    if budget_comparison:
        for budget in budget_comparison:
            progress = min(budget['actual'] / budget['budgeted'], 1.0) if budget['budgeted'] > 0 else 0
            
            col1, col2 = st.columns([3, 1])
            with col1:
                budget_emoji = get_category_emoji(budget['category'])
                st.write(f"**{budget_emoji} {budget['category']}**")
                st.progress(progress)
                st.write(f"€{budget['actual']:.2f} / €{budget['budgeted']:.2f}")
            with col2:
                if budget['remaining'] >= 0:
                    st.success(f"€{budget['remaining']:.2f} left")
                else:
                    st.error(f"€{abs(budget['remaining']):.2f} over")
    else:
        st.info("Set up your budget to see spending overview here.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def add_grocery_item():
    st.header("➕ Add Grocery Item")
    
    with st.form("add_item_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Item Name*", placeholder="e.g., Organic Bananas")
            category = st.selectbox("Category*", get_category_suggestions())
            price = st.number_input("Price (€)*", min_value=0.01, step=0.01, format="%.2f")
            quantity = st.number_input("Quantity*", min_value=1, step=1)
        
        with col2:
            unit = st.selectbox("Unit", ["pieces", "kg", "lbs", "liters", "gallons", "boxes", "bottles"])
            brand = st.text_input("Brand (optional)", placeholder="e.g., Organic Valley")
            expiry_date = st.date_input("Expiry Date (optional)", value=None)
        
        submitted = st.form_submit_button("Add Item", type="primary")
        
        if submitted:
            if name and category and price and quantity:
                new_item = {
                    'name': name,
                    'category': category,
                    'price': price,
                    'quantity': quantity,
                    'unit': unit,
                    'date_added': datetime.now().strftime("%Y-%m-%d"),
                    'expiry_date': expiry_date.strftime("%Y-%m-%d") if expiry_date else None,
                    'brand': brand if brand else None
                }
                
                st.session_state.grocery_items.append(new_item)
                save_user_data(st.session_state.username, st.session_state.grocery_items, st.session_state.budget_entries)
                st.success(f"Added {name} to your grocery list!")
                st.rerun()
            else:
                st.error("Please fill in all required fields marked with *")

def show_grocery_list():
    st.header("📝 Grocery List")
    
    if not st.session_state.grocery_items:
        st.info("Your grocery list is empty. Add some items to get started!")
        return
    
    # Search and filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("🔍 Search items", placeholder="Search by name...")
    
    with col2:
        categories = ["All"] + list(set(item['category'] for item in st.session_state.grocery_items))
        selected_category = st.selectbox("Filter by category", categories)
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Date Added", "Name", "Price", "Category"])
    
    # Filter items
    filtered_items = st.session_state.grocery_items.copy()
    
    if search_term:
        filtered_items = [item for item in filtered_items if search_term.lower() in item['name'].lower()]
    
    if selected_category != "All":
        filtered_items = [item for item in filtered_items if item['category'] == selected_category]
    
    # Sort items
    if sort_by == "Date Added":
        filtered_items.sort(key=lambda x: x['date_added'], reverse=True)
    elif sort_by == "Name":
        filtered_items.sort(key=lambda x: x['name'])
    elif sort_by == "Price":
        filtered_items.sort(key=lambda x: x['price'], reverse=True)
    elif sort_by == "Category":
        filtered_items.sort(key=lambda x: x['category'])
    
    # Display items
    if filtered_items:
        for i, item in enumerate(filtered_items):
            item_emoji = get_item_emoji(item['name'])
            with st.expander(f"{item_emoji} {item['name']} - €{item['price']:.2f} x {item['quantity']} {item['unit']}"):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    category_emoji = get_category_emoji(item['category'])
                    st.write(f"**Category:** {category_emoji} {item['category']}")
                    st.write(f"**Total Cost:** €{item['price'] * item['quantity']:.2f}")
                    if item['brand']:
                        st.write(f"**Brand:** {item['brand']}")
                
                with col2:
                    st.write(f"**Date Added:** {item['date_added']}")
                    if item['expiry_date']:
                        st.write(f"**Expires:** {item['expiry_date']}")
                
                with col3:
                    if st.button("🗑️ Remove", key=f"remove_{i}"):
                        st.session_state.grocery_items.remove(item)
                        save_user_data(st.session_state.username, st.session_state.grocery_items, st.session_state.budget_entries)
                        st.rerun()
        
        # Summary
        total_cost = sum(item['price'] * item['quantity'] for item in filtered_items)
        st.markdown("---")
        st.write(f"**Total items:** {len(filtered_items)} | **Total cost:** €{total_cost:.2f}")
    else:
        st.warning("No items match your search criteria.")

def budget_manager():
    st.header("💰 Budget Manager")
    
    current_month = datetime.now().strftime("%Y-%m")
    
    # Add/Edit Budget
    st.subheader("Set Monthly Budget")
    
    with st.form("budget_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            budget_category = st.selectbox("Category", get_category_suggestions())
            allocated_amount = st.number_input("Allocated Amount (€)", min_value=0.01, step=0.01)
        
        with col2:
            month = st.text_input("Month (YYYY-MM)", value=current_month)
        
        if st.form_submit_button("Set Budget"):
            # Check if budget already exists for this category and month
            existing_budget = None
            for i, budget in enumerate(st.session_state.budget_entries):
                if budget['category'] == budget_category and budget['month'] == month:
                    existing_budget = i
                    break
            
            new_budget = {
                'category': budget_category,
                'allocated_amount': allocated_amount,
                'spent_amount': 0,
                'month': month
            }
            
            if existing_budget is not None:
                st.session_state.budget_entries[existing_budget] = new_budget
                st.success(f"Updated budget for {budget_category}")
            else:
                st.session_state.budget_entries.append(new_budget)
                st.success(f"Added budget for {budget_category}")
            
            save_user_data(st.session_state.username, st.session_state.grocery_items, st.session_state.budget_entries)
            st.rerun()
    
    # Current Month Budget Overview
    st.subheader(f"Budget Overview - {current_month}")
    
    budget_comparison = get_budget_vs_actual()
    
    if budget_comparison:
        df = pd.DataFrame(budget_comparison)
        
        # Budget vs Actual Chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Budgeted',
            x=df['category'],
            y=df['budgeted'],
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name='Actual Spent',
            x=df['category'],
            y=df['actual'],
            marker_color='salmon'
        ))
        
        fig.update_layout(
            title='Budget vs Actual Spending',
            xaxis_title='Category',
            yaxis_title='Amount (€)',
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Budget Table
        st.subheader("Detailed Budget Breakdown")
        
        # Color code the remaining budget
        def color_remaining(val):
            if val < 0:
                return 'color: red'
            elif val < 50:
                return 'color: orange'
            else:
                return 'color: green'
        
        styled_df = df.style.applymap(color_remaining, subset=['remaining'])
        st.dataframe(styled_df, use_container_width=True)
        
    else:
        st.info("No budgets set for this month. Add some budget categories above!")

def show_analytics():
    st.header("📈 Analytics")
    
    if not st.session_state.grocery_items:
        st.info("Add some grocery items to see analytics!")
        return
    
    # Spending by Category
    st.subheader("Spending by Category")
    category_spending = get_spending_by_category()
    
    if category_spending:
        fig_pie = px.pie(
            values=list(category_spending.values()),
            names=list(category_spending.keys()),
            title="Spending Distribution by Category"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Spending Over Time
    st.subheader("Spending Trends")
    
    # Create daily spending data
    daily_spending = {}
    for item in st.session_state.grocery_items:
        date = item['date_added']
        amount = item['price'] * item['quantity']
        daily_spending[date] = daily_spending.get(date, 0) + amount
    
    if daily_spending:
        dates = list(daily_spending.keys())
        amounts = list(daily_spending.values())
        
        fig_line = px.line(
            x=dates,
            y=amounts,
            title="Daily Spending Trend",
            labels={'x': 'Date', 'y': 'Amount Spent (€)'}
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Top Expensive Items
    st.subheader("Most Expensive Items")
    
    expensive_items = sorted(
        st.session_state.grocery_items,
        key=lambda x: x['price'] * x['quantity'],
        reverse=True
    )[:10]
    
    if expensive_items:
        expensive_df = pd.DataFrame([
            {
                'Item': f"{get_item_emoji(item['name'])} {item['name']}",
                'Category': f"{get_category_emoji(item['category'])} {item['category']}",
                'Unit Price': f"€{item['price']:.2f}",
                'Quantity': f"{item['quantity']} {item['unit']}",
                'Total Cost': f"€{item['price'] * item['quantity']:.2f}"
            }
            for item in expensive_items
        ])
        
        st.dataframe(expensive_df, use_container_width=True)
    
    # Shopping Frequency by Category
    st.subheader("Shopping Frequency by Category")
    
    category_frequency = {}
    for item in st.session_state.grocery_items:
        category = item['category']
        category_frequency[category] = category_frequency.get(category, 0) + 1
    
    if category_frequency:
        fig_bar = px.bar(
            x=list(category_frequency.keys()),
            y=list(category_frequency.values()),
            title="Number of Items Purchased by Category",
            labels={'x': 'Category', 'y': 'Number of Items'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

def show_recommendations():
    st.header("🎯 Smart Recommendations")
    
    if not st.session_state.grocery_items:
        st.info("Add some grocery items to get personalized recommendations!")
        return
    
    # Budget recommendations
    st.subheader("💡 Budget Recommendations")
    
    budget_comparison = get_budget_vs_actual()
    if budget_comparison:
        for budget in budget_comparison:
            if budget['remaining'] < 0:
                st.warning(f"⚠️ You're €{abs(budget['remaining']):.2f} over budget in {budget['category']}. Consider reducing spending in this category.")
            elif budget['remaining'] < budget['budgeted'] * 0.1:
                st.info(f"💡 You have only €{budget['remaining']:.2f} left in {budget['category']}. Plan your remaining purchases carefully.")
    
    # Shopping pattern recommendations
    st.subheader("🛍️ Shopping Pattern Insights")
    
    category_spending = get_spending_by_category()
    total_spending = sum(category_spending.values())
    
    if total_spending > 0:
        largest_category = max(category_spending, key=category_spending.get)
        largest_percentage = (category_spending[largest_category] / total_spending) * 100
        
        st.info(f"📊 Your largest spending category is **{largest_category}** ({largest_percentage:.1f}% of total spending)")
        
        if largest_percentage > 40:
            st.warning(f"💡 Consider diversifying your spending - {largest_category} takes up a large portion of your budget.")
    
    # Price optimization suggestions
    st.subheader("💰 Price Optimization Tips")
    
    expensive_items = sorted(
        st.session_state.grocery_items,
        key=lambda x: x['price'],
        reverse=True
    )[:5]
    
    st.write("**Most expensive items in your list:**")
    for item in expensive_items:
        item_emoji = get_item_emoji(item['name'])
        st.write(f"• {item_emoji} {item['name']} - €{item['price']:.2f}")
    
    st.info("💡 Consider looking for alternatives or buying these items in bulk when on sale.")
    
    # Expiry date alerts
    st.subheader("⏰ Expiry Alerts")
    
    expiring_soon = []
    today = datetime.now().date()
    
    for item in st.session_state.grocery_items:
        if item['expiry_date']:
            expiry = datetime.strptime(item['expiry_date'], "%Y-%m-%d").date()
            days_until_expiry = (expiry - today).days
            
            if days_until_expiry <= 7:
                expiring_soon.append((item, days_until_expiry))
    
    if expiring_soon:
        st.warning("⚠️ Items expiring soon:")
        for item, days in expiring_soon:
            item_emoji = get_item_emoji(item['name'])
            if days < 0:
                st.error(f"• {item_emoji} {item['name']} expired {abs(days)} days ago")
            elif days == 0:
                st.error(f"• {item_emoji} {item['name']} expires today!")
            else:
                st.warning(f"• {item_emoji} {item['name']} expires in {days} days")
    else:
        st.success("✅ No items expiring in the next 7 days!")
    
    # Seasonal recommendations
    st.subheader("🌱 Seasonal Tips")
    
    current_month = datetime.now().month
    
    seasonal_tips = {
        1: "Winter produce: Root vegetables, citrus fruits, and hearty greens are in season and typically cheaper.",
        2: "Winter produce: Root vegetables, citrus fruits, and hearty greens are in season and typically cheaper.",
        3: "Spring produce: Asparagus, artichokes, and spring onions are coming into season.",
        4: "Spring produce: Fresh herbs, lettuce, and early berries are at their best.",
        5: "Spring to summer: Strawberries, rhubarb, and spring vegetables are in peak season.",
        6: "Summer produce: Berries, stone fruits, and summer squash are in season and affordable.",
        7: "Peak summer: Tomatoes, corn, and summer fruits are at their best and cheapest.",
        8: "Late summer: Peaches, plums, and summer vegetables are still in season.",
        9: "Fall harvest: Apples, pears, and root vegetables are coming into season.",
        10: "Fall produce: Pumpkins, squash, and late-season fruits are at their peak.",
        11: "Late fall: Cranberries, sweet potatoes, and winter squash are in season.",
        12: "Winter produce: Citrus fruits and hearty vegetables are in peak season."
    }
    
    st.info(f"🌿 {seasonal_tips.get(current_month, 'Check what\'s in season for better prices!')}")

if __name__ == "__main__":
    main()
