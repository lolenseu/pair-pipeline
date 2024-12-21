import os
import json
import requests
from flask import Flask, jsonify, request


# Variables
app = Flask(__name__)

parent_folder: str = './pipeline'
megastream_forlder: str = './megastream'


# Functions
def create_id(pipeline_id: str, pipeline_key: str) -> bool:    
    hex_folder_name = hex(int(pipeline_id))
    folder_location = os.path.join(parent_folder, hex_folder_name)
    try:
        if not os.path.exists(parent_folder):
            os.makedirs(parent_folder)
        if not os.path.isdir(folder_location):
            os.mkdir(folder_location)
        
        key_file_path = os.path.join(folder_location, 'key.txt')
        with open(key_file_path, 'a') as key_file:
            key_file.write(pipeline_key)
        
        if os.path.isdir(folder_location) and os.path.exists(key_file_path):
            return True
        else:
            return False
    except:
        return False
        
def confirm_id(pipeline_id: str) -> bool:
    hex_folder_name = hex(int(pipeline_id))
    folder_location = os.path.join(parent_folder, hex_folder_name)
    return os.path.isdir(folder_location)

def confirm_key(pipeline_id: str) -> str:
    hex_folder_name = hex(int(pipeline_id))
    folder_location = os.path.join(parent_folder, hex_folder_name)
    key_file_path = os.path.join(folder_location, 'key.txt')
    with open(key_file_path, 'r') as file:
            file_key = file.read()
    return file_key

def data_available(pipeline_id: str) -> bool:
    hex_folder_name = hex(int(pipeline_id))
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
@app.route('/', methods=['GET', 'POST'])
def home():
    response = {'message': 'Welcome to Pair-Pipeline!'}
    return jsonify(response), 200

@app.route('/megastream', methods=['GET', 'POST'])
def megastream():
    id: int = total_id()
    server_ip: str = get_public_ip()
    megasteam: dict = {
        'server_ip': server_ip,
        'total_id': id
        }
    return jsonify(megasteam), 200

@app.route('/pipeline/create', methods=['GET', 'POST'])
def pipeline_create():
    try:
        pipeline_id: str = request.args.get('id')
        pipeline_key: str = request.args.get('key')
        
        if confirm_id(pipeline_id):
            response = {'error': 'ID already exists'}
            return jsonify(response), 400    
        else:
            create_id(pipeline_id, pipeline_key)
            response = {'message': 'Pipeline created successfully', 'id': pipeline_id}
            return jsonify(response), 201   
    except:
        response = {'error': 'Invalid request'}
        return jsonify(response), 400

@app.route('/pipeline/send', methods=['GET', 'POST'])
def pipeline_send():
    try:
        pipeline_id: str = request.args.get('id')
        pipeline_key: str = request.args.get('key')   
        int_virtual_data: dict[str, int] = {}
        str_virtual_data: dict[str, str] = {}
        response = {}
             
        # Check if pipeline_id is exactly 8 digits long
        if len(pipeline_id) != 8 and pipeline_id.isdigit():
            response = {'error': 'ID must be exactly 8 digits long'}
            return jsonify(response), 400           
        
        # check if pipeline_key
        if len(pipeline_id) != 16 and pipeline_key != confirm_key(pipeline_id):
            response = {'error': 'Wrong key'}
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

        for x in int_virtual_data:
            int_count: int = 4
            if len(str(int_virtual_data[x])) > int_count:
                response = {'error': f'Integer limit {int_count} digits for {x}'}
                return jsonify(response), 400

        for x in str_virtual_data:
            str_count: int = 256
            if len(str_virtual_data[x]) > str_count:
                response = {'error': f'String limit {str_count} characters for {x}'}
                return jsonify(response), 400

        if int_virtual_data or str_virtual_data:
            store_data(pipeline_id, {**int_virtual_data, **str_virtual_data})
            response = {'message': 'Data stored successfully', 'id': pipeline_id}
            return jsonify(response), 201
        else:
            response = {'error': 'Data not stored', 'id': pipeline_id}
            return jsonify(response), 201    
    except:
        response = {'error': 'Invalid request'}
        return jsonify(response), 400

@app.route('/pipeline/receive', methods=['GET', 'POST'])
def pipeline_receive():
    try:
        pipeline_id: str = request.args.get('id')
        pipeline_key: str = request.args.get('key')
        
        if confirm_id(pipeline_id):
            if confirm_key(pipeline_id) != pipeline_key:
                response = {'error': 'Wrong key'}
                return jsonify(response), 400
            
            if data_available(pipeline_id):
                data = read_data(pipeline_id)
                response = {'message': 'Data retrieved successfully', 'id': pipeline_id, 'stream': data}
            else:
                response = {'error': 'Data not retrieved'}
            
            return jsonify(response), 200
        else:
            response = {'error': 'ID not found'}
            return jsonify(response), 400
    except:
        response = {'error': 'Invalid request'}
        return jsonify(response), 400

@app.errorhandler(404)
def page_not_found(e):
    response = {'error': 'Invalid request'}
    return jsonify(response), 404


# Main
if __name__ == '__main__':
    app.run(debug=True) # disable debug in production
    #app.run(host='0.0.0.0', port=5000)  # Change the port number if needed