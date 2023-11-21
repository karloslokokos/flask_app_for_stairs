from flask import Flask, request,jsonify
from flask_cors import CORS
import mysql.connector
import json

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


#cors = CORS(app, resources={r"/get_data": {"origins": "http://localhost:3000"}})

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "musical_stairs",
    "port": "8889"
    
}

def insert_data_into_mysql(message):
    #data = json.dumps({"topic": topic, "message": message})  # Convert topic and message to JSON format
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Define the SQL query to insert data into the table
        insert_query = "INSERT INTO mqtt_messages (notes_data) VALUES (%s)"

        # Execute the query with the data
        cursor.execute(insert_query, (message,))
        connection.commit()

        cursor.close()
        connection.close()

        print("Data inserted into MySQL successfully")
    except mysql.connector.Error as error:
        print(f"Error: {error}")

@app.route('/mqtt', methods=['POST'])
def receive_mqtt_message():
    #topic = request.form.get('topic')
    message = request.form.get('message')
    
    # print topic and message receieved
    print( message)

    #insert data into database

    insert_data_into_mysql(message)
    
    return 'Message received'

@app.route('/get_data', methods=['GET'])
def get_data_from_mysql():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Define the SQL query to retrieve data from the table
        select_query = "SELECT id, timestamp, notes_data FROM mqtt_messages"

        # Execute the query
        cursor.execute(select_query)

        # Fetch all the data
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        # Convert data to a list of dictionaries
        data_list = [{'id': row[0], 'timestamp': row[1], 'message': row[2]} for row in data]

        print(data_list)

        return jsonify(data_list)
    except mysql.connector.Error as error:
        print(f"Error: {error}")

        
def fetch_note_data_from_mysql():
    print("Fetching note data from MySQL")

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Define the SQL query to retrieve only the notes_data column
        select_query = "SELECT notes_data FROM mqtt_messages"

        # Execute the query
        cursor.execute(select_query)

        # Fetch all the data
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        # Extract the notes_data column values
        note_data = [row[0] for row in data]

        # Convert the flat list into an array of arrays containing 4 notes each
        grouped_notes = [note_data[i:i+4] for i in range(0, len(note_data), 4)]

        #print("Note data fetched from MySQL:", grouped_notes)
        return grouped_notes
    except mysql.connector.Error as error:
        print(f"Error: {error}")
        return []

@app.route('/get_note_data', methods=['GET'])
def get_note_data_from_mysql():
    note_data = fetch_note_data_from_mysql()
    # Wrap the note_data in a dictionary
    return jsonify(note_data)
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
