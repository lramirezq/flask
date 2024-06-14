from flask import Flask, request, jsonify
import serverless_wsgi
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("events.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

events_list = [
    {
        "id": 0,
        "event_type": "pull_request",
        "event_name": "change_event"
    },
    {
        "id": 1,
        "event_type": "release",
        "event_name": "deployment_event"
    },
    {
        "id": 2,
        "event_type": "push",
        "event_name": "workflow_event"
    },
    {
        "id": 3,
        "event_type": "pull_request_merged",
        "event_name": "deployment_event"
    }
]

@app.route('/events', methods=['GET', 'POST'])
def events():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        if len(events_list) > 0:
            return jsonify(events_list)
        else:
            return 'Event not found', 404
  
    if request.method == 'POST':
        new_event_type = request.json['event_type']
        new_event_name = request.json['event_name']

        sql = """INSERT INTO event (event_type, event_name)
                 VALUES (?, ?)"""
        cursor.execute(sql, (new_event_type, new_event_name))
        conn.commit()

        event_id = cursor.lastrowid

        new_obj = {
            'id': event_id,
            'event_type': new_event_type,
            'event_name': new_event_name
        }

        events_list.append(new_obj)
        return jsonify(new_obj), 201

@app.route('/event/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_event_workflow(id):
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        for event in events_list:
            if event['id'] == id:
                return jsonify(event)
        return 'Event not found', 404
    
    if request.method == 'PUT':
        new_event_type = request.json['event_type']
        new_event_name = request.json['event_name']

        sql = """UPDATE event
                 SET event_type = ?,
                     event_name = ?
                 WHERE id = ?"""
        cursor.execute(sql, (new_event_type, new_event_name, id))
        conn.commit()

        for event in events_list:
            if event['id'] == id:
                event['event_type'] = new_event_type
                event['event_name'] = new_event_name
                updated_event = {
                    'id': id,
                    'event_type': new_event_type,
                    'event_name': new_event_name
                }
                return jsonify(updated_event)
        return 'Event not found', 404
    
    if request.method == 'DELETE':
        sql = """DELETE FROM event WHERE id = ?"""
        cursor.execute(sql, (id,))
        conn.commit()

        for event in events_list:
            if event['id'] == id:
                events_list.remove(event)
                return 'Event deleted successfully', 200
        return 'Event not found', 404

#funcion para AWS Lambda
def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

@app.route('/version', methods=['GET'])
def version():
    return jsonify("Version LRQ")
    
    
if __name__ == '__main__':
    app.run(debug=True)
