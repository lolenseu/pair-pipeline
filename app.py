from flask import Flask, jsonify, request


app = Flask(__name__)


data = {
    'items': [
        {'id': 1, 'name': 'Item 1'},
        {'id': 2, 'name': 'Item 2'}
    ]
}


@app.route('/')
def home():
    return "Welcome to Pair-Pipeline!"


@app.route('/pair/api/items', methods=['GET'])
def get_items():
    return jsonify(data)

@app.route('/pair/api', methods=['GET'])
def pair():
    item = next((item for item in data['items'] if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/pipeline/api', methods=['POST']))
def pipeline():
    new_item = request.get_json()
    new_item['id'] = len(data['items']) + 1
    data['items'].append(new_item)
    return jsonify(new_item), 201


if __name__ == '__main__':
    app.run(debug=True)