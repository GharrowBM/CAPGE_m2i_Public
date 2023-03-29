from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'todo_db'

# Initialize MySQL
mysql = MySQL(app)

# Routes
@app.route('/todoitems', methods=['GET'])
def get_todo_items():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM todo_items")
    rows = cur.fetchall()
    todo_items = []
    for row in rows:
        todo_item = {'id': row[0], 'title': row[1], 'description': row[2], 'is_completed': row[3]}
        todo_items.append(todo_item)
    cur.close()
    return jsonify(todo_items)

@app.route('/todoitems', methods=['POST'])
def create_todo_item():
    title = request.json['title']
    description = request.json['description']
    is_completed = request.json['is_completed']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO todo_items (title, description, is_completed) VALUES (%s, %s, %s)", (title, description, is_completed))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Todo item created'})

@app.route('/todoitems/<int:todo_item_id>', methods=['PUT'])
def update_todo_item(todo_item_id):
    title = request.json['title']
    description = request.json['description']
    is_completed = request.json['is_completed']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE todo_items SET title=%s, description=%s, is_completed=%s WHERE id=%s", (title, description, is_completed, todo_item_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Todo item updated'})

@app.route('/todoitems/<int:todo_item_id>', methods=['DELETE'])
def delete_todo_item(todo_item_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM todo_items WHERE id=%s", (todo_item_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Todo item deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
