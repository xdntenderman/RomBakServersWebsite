from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__)
CORS(app)

# Database file path
DB_PATH = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            account_role TEXT,
            job_role TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return "Backend RomBak Servers is Running!"

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    acc_role = data.get('accountRole')
    job_role = data.get('jobRole')

    hashed_pw = generate_password_hash(password)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, email, password, account_role, job_role) VALUES (?, ?, ?, ?, ?)', 
                       (username, email, hashed_pw, acc_role, job_role))
        conn.commit()
        conn.close()
        return jsonify({"message": "Register berhasil!"}), 201
    except Exception as e:
        return jsonify({"message": "Username/Email sudah ada!"}), 400

if __name__ == '__main__':
    # Render butuh port dinamis
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
