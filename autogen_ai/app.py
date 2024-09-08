from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data to return
user_data = [
    {"name": "zhangsan", "num": "00991"},
    {"name": "lisi", "num": "00995"}
]

map_data = [
    {"country": "china", "capital": "beijing"},
    {"country": "japan", "capital": "tokyo"}
]


@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    # Get the 'msg' parameter from the request
    msg = request.args.get('msg')

    # You can add logic to filter or handle the 'msg' parameter if needed
    if msg and msg != 'all':
        result = [entry for entry in user_data if msg in entry['name'] or msg in entry['num']]
        return jsonify(result)
    else:
        return jsonify(user_data)


@app.route('/get_map_data', methods=['GET'])
def get_map_data():
    # Get the 'msg' parameter from the request
    msg = request.args.get('msg')

    if msg and msg != 'all':
        result = [entry for entry in map_data if msg in entry['country'] or msg in entry['capital']]
        return jsonify(result), 200
    else:
        return jsonify(map_data), 200


if __name__ == '__main__':
    app.run(debug=True)
