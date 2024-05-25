#!/usr/bin/python3


from flask import Flask, request, jsonify, session 
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import string, random, secrets
import sqlite3
from functools import wraps


# Initialize flask app
app = Flask(__name__)
app.secret_key = 'Pass_Gen.Secret?Key1.0' 
CORS(app)

# Initialize database
def init_db():
    # Create a database connection and cursor object to execute commands
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    
    # Create a table to store users
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT)''')

    # Create a table with foreign key to users table
    c.execute('''CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    username TEXT,
                    password TEXT,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id))''')

    conn.commit()
    conn.close()

init_db()


@app.route('/', methods=['GET','POST'])
def passgen():
        data = request.get_json()

        length = data.get('length')
        has_lower = data.get('hasLower')
        has_upper = data.get('hasUpper')
        has_digits = data.get('hasDigits')
        has_symbols = data.get('hasSymbols')
    
        char_list = ""

        if(has_lower):
            char_list += string.ascii_lowercase

        if(has_upper):
            char_list += string.ascii_uppercase

        if(has_digits):
            char_list += string.digits

        if(has_symbols):
            char_list += string.punctuation

        result = []

        for i in range (length):
            randomChar = secrets.choice(char_list)
            result.append(randomChar)

        password = "".join(result)
        return jsonify({'password': password})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    hashed_password = generate_password_hash(password, method='sha256')

    try:
        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        # Insert new user into user table
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username already exists'}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    # Select user from the users table
    c.execute("SELECT * FROM users WHERE username=?)", (username,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[2], password):
        session['user_id'] = user[0] # Store user ID in session
        return jsonify({'message': 'Login successfully'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None) # Remove user ID from session
    return jsonify({'message': 'Logged out successfully'}), 200

# Decorator to protect routes that require authentication
def login_required(f):
    @wraps(f) 
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/passwords', methods=['GET'])
@login_required
def get_passwords():
    user_id = session['user_id']
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    # Select password for the logged-in user
    c.execute("SELECT * FROM passwords WHERE user_id=?", (user_id,))
    passwords = c.fetchall()
    conn.close()
    return jsonify({'passwords': passwords})

@app.route('/passwords', methods=['POST'])
@login_required
def save_passwords():
    data = request.get_json
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    user_id = session['user_id']

    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    # Insert new password entry into the passwords table
    c.execute("INSERT INTO passwords (name, username, password, user_id) VALUES (?, ?, ?, ?)", (name, username, password, user_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Password saved successfully'})

@app.route('/passwords/<int:id>', methods=['DELETE'])
def delete_password(id):
    user_id = session['user_id']
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()


    c.execute("DELETE FROM passwords WHERE id = ? AND user_id = ?", (id,user_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Password deleted successfully'})

if __name__ == "__main__":
    app.run(debug=True)
