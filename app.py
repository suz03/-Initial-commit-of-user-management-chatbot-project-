from flask import Flask, request, jsonify, send_from_directory
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234567890'
app.config['MYSQL_DB'] = 'user'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    print("Form Data Received:")
    for key, value in request.form.items():
        print(f"{key}: {value}")

    name = request.form['name']
    city = request.form['city']
    age = request.form['age']
    email = request.form['email']
    phone_number = request.form['phone_number']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "INSERT INTO user_data (name, city, age, email, phone_number) VALUES (%s, %s, %s, %s, %s)",
        (name, city, age, email, phone_number)
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "User added successfully"}), 201

@app.route('/get_users', methods=['GET'])
def get_users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM user_data")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)

@app.route('/view_users')
def view_users():
    return send_from_directory(os.getcwd(), 'view_users.html')

if __name__ == '__main__':
    app.run(debug=True)
