from flask import Flask, jsonify
import datetime
import redis_api
import mongodb_api

if __name__ == "__main__":

    app = Flask(__name__)

    @app.route('/ping', methods=['GET'])
    def ping_route():
        return jsonify(redis_api.ping())
    
    @app.route('/connect/<username>', methods=['POST'])
    def connect_route(username):
        return jsonify(redis_api.connect(username))

    @app.route('/disconnect/<username>', methods=['POST'])
    def disconnect_route(username):
        return jsonify(redis_api.disconnect(username))

    @app.route('/register/<username>/<password>', methods=['POST'])
    def register_route(username, password):
        return jsonify(redis_api.register(username, password))
    
    @app.route('/user_count', methods=['GET'])
    def user_count_route():
        return jsonify(redis_api.get_user_count())

    @app.route('/user_list', methods=['GET'])
    def user_list_route():
        return jsonify(redis_api.get_user_list())

    @app.route('/send_message/<text>/<sender_id>/<target_id>', methods=['POST'])
    def send_message_route(text, sender_id, date, target_id):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        return jsonify(mongodb_api.send_message(text, sender_id, date, target_id))
    
    @app.route('/get_messages/<group_id>', methods=['GET'])
    def get_messages_route(group_id):
        return jsonify(mongodb_api.get_messages(group_id))

    port = 5000
    app.run(host='0.0.0.0', port=port)