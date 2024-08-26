from flask import Blueprint, request, jsonify, session
from datetime import datetime
from auth import create_connection

history = Blueprint('history', __name__)

def save_history(user_id, input_text, normalized_text, translated_text):
    connection = create_connection()
    cursor = connection.cursor()
    
    query = "INSERT INTO user_history (user_id, input_text, normalized_text, translated_text, timestamp) VALUES (%s, %s, %s, %s, NOW())"
    values = (user_id, input_text, normalized_text, translated_text)
    cursor.execute(query, values)
    
    connection.commit()
    cursor.close()
    connection.close()


@history.route('/save', methods=['POST'])
def save_user_history():
    data = request.get_json()
    user_id = session.get('user_id')
    input_text = data.get('input_text')
    normalized_text = data.get('normalized_text')
    translated_text = data.get('translated_text')
    
    save_history(user_id, input_text, normalized_text, translated_text)
    
    return jsonify({'status': 'success'}), 200

@history.route('/get', methods=['GET'])
def get_user_history():
    user_id = session.get('user_id')
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT input_text, normalized_text, translated_text, timestamp FROM user_history WHERE user_id = %s ORDER BY timestamp DESC"
    cursor.execute(query, (user_id,))
    history = cursor.fetchall()

    history_list = []
    for record in history:
        history_item = {
            'input_text': record[0],
            'normalized_text': record[1],
            'translated_text': record[2],
            'timestamp': record[3].strftime('%Y-%m-%d %H:%M:%S') if record[3] else None
        }
        history_list.append(history_item)

    cursor.close()
    connection.close()
    
    return jsonify(history_list)


@history.route('/clear', methods=['DELETE'])
def clear_user_history():
    user_id = session.get('user_id')
    connection = create_connection()
    cursor = connection.cursor()
    
    try:

        cursor.execute("TRUNCATE TABLE user_history")
        connection.commit()
        return jsonify({'message': 'History cleared successfully'}), 200
    except Exception as e:
        print(f"Error clearing history: {e}")
        return jsonify({'message': 'Failed to clear history'}), 500
    finally:
        cursor.close()
        connection.close()
