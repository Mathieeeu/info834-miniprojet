from flask import Flask, jsonify
from flask_cors import CORS
import datetime
import redis_api
import mongodb_api

if __name__ == "__main__":

    app = Flask(__name__)
    CORS(app) # Ajoute CORS pour permettre les requêtes cross-origin

    # > curl -X GET http://localhost:5000
    @app.route('/')
    def home():
        return "API is running letsgooooooooooo!"

    # > curl -X GET http://localhost:5000/ping
    @app.route('/ping', methods=['GET'])
    def ping_route():
        return jsonify(redis_api.ping())
    
    # > curl -X POST http://localhost:5000/clear_user_data
    @app.route('/clear_user_data', methods=['POST'])
    def clear_user_data_route():
        return jsonify(redis_api.clear_user_data())
    
    # > curl -X POST http://localhost:5000/disconnect/<username>
    @app.route('/disconnect/<username>', methods=['POST'])
    def disconnect_route(username):
        username = username.lower()
        return jsonify(redis_api.disconnect(username))

    # > curl -X POST http://localhost:5000/register/<username>/<password>
    @app.route('/register/<username>/<password>', methods=['POST'])
    def register_route(username, password):
        username = username.lower()
        return jsonify(redis_api.register(username, password))
    
    # > curl -X POST http://localhost:5000/login/<username>/<password>
    @app.route('/login/<username>/<password>', methods=['POST'])
    def login_route(username, password):
        username = username.lower()
        return jsonify(redis_api.login(username, password))
    
    # > curl -X GET http://localhost:5000/user_count
    @app.route('/user_count', methods=['GET'])
    def user_count_route():
        return jsonify(redis_api.get_user_count())

    # > curl -X GET http://localhost:5000/user_list
    @app.route('/user_list', methods=['GET'])
    def user_list_route():
        return jsonify(redis_api.get_user_list())
    
    # > curl -X GET http://localhost:5000/online_user_count
    @app.route('/online_user_count', methods=['GET'])
    def online_user_count_route():
        return jsonify(redis_api.get_online_user_count())
    
    # > curl -X GET http://localhost:5000/online_user_list
    @app.route('/online_user_list', methods=['GET'])
    def online_user_list_route():
        return jsonify(redis_api.get_online_user_list())

    # > curl -X POST http://localhost:5000/send_message/<text>/<sender_name>/<reciever_name>
    @app.route('/send_message/<text>/<sender_name>/<reciever_name>', methods=['POST'])
    def send_message_route(text, sender_name, reciever_name):
        sender_name = sender_name.lower()
        reciever_name = reciever_name.lower()
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        return jsonify(mongodb_api.send_message(text, sender_name, date, reciever_name))
    
    # > curl -X GET http://localhost:5000/get_messages/<reciever_name>
    @app.route('/get_messages/<reciever_name>', methods=['GET'])
    def get_messages_route(reciever_name):
        reciever_name = reciever_name.lower()
        return jsonify(mongodb_api.get_messages(reciever_name))

    port = 5000
    app.run(host='0.0.0.0', port=port)