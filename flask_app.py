import os
import json
import requests
from flask import Flask, jsonify, request

# Variables
app = Flask(__name__)

parent_folder: str = './pipeline'
megastream_forlder: str = './megastream'


# Functions
def make_folder_location(pipeline_id: str) -> bool:
    hex_folder_name = hex(int(pipeline_id))
    folder_location = os.path.join(parent_folder, hex_folder_name)
    
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)
    if not os.path.isdir(folder_location):
        os.mkdir(folder_location)
        
    return True
        
def confirm_folder_location(pipeline_id: str) -> bool:
    hex_folder_name = hex(int(pipeline_id))
    folder_location = os.path.join(parent_folder, hex_folder_name)
    return os.path.isdir(folder_location)

def data_available(id: str) -> bool:
    hex_folder_name = hex(int(id))
    file_path = os.path.join(parent_folder, hex_folder_name, 'stream.json')
    return os.path.exists(file_path)

def store_data(id: str, data: dict) -> None:
    hex_folder_name = hex(int(id))
    folder_location = os.path.join(parent_folder, hex_folder_name)
    if not os.path.exists(folder_location):
        os.makedirs(folder_location)
    with open(os.path.join(folder_location, 'stream.json'), 'w') as f:
        json.dump(data, f)

def read_data(id: str) -> dict:
    hex_folder_name = hex(int(id))
    folder_location = os.path.join(parent_folder, hex_folder_name)
    with open(os.path.join(folder_location, 'stream.json'), 'r') as f:
        return json.load(f)
    
def total_id() -> int:
    return len(os.listdir(parent_folder))

def get_public_ip() -> str:
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json()['ip']
    except requests.RequestException:
        return 'Unable to get IP'


# Routes
@app.route('/')
def home():
    response = {'message': 'Welcome to Pair-Pipeline!'}
    return jsonify(response), 200

@app.route('/megastream', methods=['GET'])
def megastream():
    id: int = total_id()
    server_ip: str = get_public_ip()
    megasteam: dict = {
        'server_ip': server_ip,
        'total_id': id
        }
    
    return jsonify(megasteam), 200

@app.route('/pipeline/send', methods=['GET', 'POST'])
def pipeline_snd():
    pipeline_id: str = request.args.get('id')
    int_virtual_data: dict[str, int] = {}
    str_virtual_data: dict[str, str] = {}
    response = {}

    # Check if pipeline_id is exactly 8 digits long
    if len(pipeline_id) == 8 and pipeline_id.isdigit():
        pass
    else:
        response = {'error': 'ID must be exactly 8 digits long'}
        return jsonify(response), 400

    # Populate int_virtual_data
    for i in range(1, 17):
        key = f'ivd{i}'
        value = request.args.get(key)
        if value:
            int_virtual_data[key] = int(value)

    # Populate str_virtual_data
    for i in range(1, 5):
        key = f'svd{i}'
        value = request.args.get(key)
        if value:
            str_virtual_data[key] = value

    folder_made = make_folder_location(pipeline_id)
    data_check: bool = True

    for x in int_virtual_data:
        int_count: int = 4
        if len(str(int_virtual_data[x])) > int_count:
            response = {'error': f'integer limit {int_count} digits for {x}'}
            data_check = False

    for x in str_virtual_data:
        str_count: int = 256
        if len(str_virtual_data[x]) > str_count:
            response = {'error': f'string limit {str_count} characters for {x}'}
            data_check = False

    if not data_check:
        return jsonify(response), 400

    if folder_made:
        if_folder_available = confirm_folder_location(pipeline_id)

        if if_folder_available:
            if int_virtual_data or str_virtual_data:
                store_data(pipeline_id, {**int_virtual_data, **str_virtual_data})
                response = {'message': 'Data stored successfully', 'id': pipeline_id}
            else:
                response = {'error': 'Data not stored', 'id': pipeline_id}
        else:
            response = {'error': 'ID not available'}

        return jsonify(response), 201
    else:
        response = {'error': 'Folder creation failed'}
        return jsonify(response), 500

@app.route('/pipeline/receive', methods=['GET'])
def pipeline_receive():
    pipeline_id: str = request.args.get('id')
    if_folder_available = confirm_folder_location(pipeline_id)
    
    if if_folder_available:
        data = read_data(pipeline_id)
        response = {'message': 'Data retrieved successfully', 'id': pipeline_id, 'stream': data}
    else:
        response = {'error': 'Data not retrieved'}
    
    return jsonify(response), 200

@app.errorhandler(404)
def page_not_found(e):
    response = {'error': 'Invalid request'}
    return jsonify(response), 404


# Main
if __name__ == '__main__':
    app.run(debug=True)