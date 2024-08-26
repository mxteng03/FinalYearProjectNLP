from flask import Blueprint, request, jsonify, render_template, redirect, url_for, make_response, session
import mysql.connector 
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()

auth = Blueprint('auth', __name__)

def create_connection():    
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS')
    )
    except Error as e:
        print(f"Error: '{e}'")  

    return connection

@auth.route('/login')
def login_page():
    return render_template('login.html')

@auth.route('/signup')
def signup_page():
    return render_template('signup.html')

@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (first_name, last_name, email, phone, password) VALUES (%s, %s, %s, %s, %s)", 
                       (first_name, last_name, email, phone, password))
        connection.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Error as e:
        print(f"Error: '{e}'")
        return jsonify({'message': 'User already exists'}), 400
    finally:
        cursor.close()
        connection.close()

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    remember = data.get('remember', False)

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if user:
        session['user_id'] = user[0]  # Store user_id in session
        response = make_response(jsonify({'message': 'Login successful', 'redirect': url_for('main_page')}), 200)
        if remember:
            response.set_cookie('email', email, max_age=timedelta(days=30))
        else:
            response.set_cookie('email', email)  # Set session cookie
        return response
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@auth.route('/logout')
def logout():
    response = make_response(redirect(url_for('auth.login_page')))
    response.set_cookie('email', '', expires=0)
    session.pop('user_id', None)
    return response

