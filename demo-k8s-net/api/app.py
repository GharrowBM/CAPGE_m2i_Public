from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

# Initialize MySQL
mysql = MySQL(app)

# Routes
@app.route('/clients', methods=['GET'])
def get_todo_items():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM clients")
    rows = cur.fetchall()
    clients = []
    for row in rows:
        client = {'id': row[0], 'firstname': row[1], 'lastname': row[2], 'email': row[3], 'phoneNumber': row[4]}
        clients.append(client)
    cur.close()
    return jsonify(clients)

@app.route('/clients', methods=['POST'])
def create_todo_item():
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    phone_number = request.json['phoneNumber']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO todo_items (firstname, lastname, email, phoneNumber) VALUES (%s, %s, %s, %s)", (firstname, lastname, email, phone_number))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Client created'})

@app.route('/clients/<int:client_id>', methods=['PUT'])
def update_todo_item(client_id):
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    phone_number = request.json['phoneNumber']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE todo_items SET firstname=%s, lastname=%s, email=%s, phoneNumber=%s WHERE id=%s", (firstname, lastname, email, phone_number, client_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Client updated'})

@app.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_todo_item(client_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM clients WHERE id=%s", (client_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Client deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
