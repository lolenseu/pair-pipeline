import os
import json
import requests
from flask import Flask, jsonify, request
from datetime import datetime

# Variables
app = Flask(__name__)

parent_folder: str = './pipeline'
megastream_folder: str = './megastream'

# Response Class
class Response:
    @staticmethod
    def error(message: str, pipeline_id: str, timestamp: str) -> tuple:
        response = {'response': 'error!', 'message': message, 'id': pipeline_id, 'timestamp': timestamp}
        return jsonify(response), 400

    @staticmethod
    def success(message: str, pipeline_id: str, timestamp: str, data: dict = None) -> tuple:
        response = {'response': 'success!', 'message': message, 'id': pipeline_id, 'timestamp': timestamp}
        if data:
            response.update(data)
        return jsonify(response), 201

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

def update_key(pipeline_id: str, pipeline_new_key: str) -> None:
    hex_folder_name = hex(int(pipeline_id))
    folder_location = os.path.join(parent_folder, hex_folder_name)
    key_file_path = os.path.join(folder_location, 'key.txt')
    with open(key_file_path, 'w') as file:
        file.write(pipeline_new_key)

def data_available(pipeline_id: str) -> bool:
    hex_folder_name = hex(int(pipeline_id))
    file_path = os.path.join(parent_folder, hex_folder_name, 'stream.json')
    return os.path.exists(file_path)

def store_data(pipeline_id: str, data: dict) -> None:
    hex_folder_name = hex(int(pipeline_id))
    folder_location = os.path.join(parent_folder, hex_folder_name)
    if not os.path.exists(folder_location):
        os.makedirs(folder_location)
    with open(os.path.join(folder_location, 'stream.json'), 'w') as f:
        json.dump(data, f)

def read_data(pipeline_id: str) -> dict:
    hex_folder_name = hex(int(pipeline_id))
    folder_location = os.path.join(parent_folder, hex_folder_name)
    with open(os.path.join(folder_location, 'stream.json'), 'r') as f:
        return json.load(f)

def total_id() -> int:
    return len(os.listdir(parent_folder))

def get_server_public_ip() -> str:
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

# Megastream
@app.route('/megastream', methods=['GET', 'POST'])
def megastream():
    server_ip: str = get_server_public_ip()
    id: int = total_id()
    timestamp = datetime.now().isoformat()
    megasteam: dict = {
        'server_ip': server_ip,
        'total_id': id,
        'timestamp': timestamp
    }
    return jsonify(megasteam), 200

# Pipeline
@app.route('/pipeline', methods=['GET', 'POST'])
def pipeline():
    try:
        pipeline_option: str = request.args.get('opt')
        pipeline_id: str = request.args.get('id')
        pipeline_key: str = request.args.get('key')
        pipeline_new_key: str = request.args.get('nkey')
        timestamp = datetime.now().isoformat()
        
        # Check if pipeline_id is exactly 8 digits long
        if len(pipeline_id) != 8 or not pipeline_id.isdigit():
            return Response.error('ID must be exactly 8 digits long', pipeline_id, timestamp)
        
        # Check if pipeline_key
        if len(pipeline_key) != 16:
            return Response.error('Key must be exactly 16 string long', pipeline_id, timestamp)
        
        # Check if pipeline_option is valid
        if pipeline_option == 'cre':
            if confirm_id(pipeline_id):
                return Response.error('ID already exists', pipeline_id, timestamp)
            else:
                create_id(pipeline_id, pipeline_key)
                return Response.success('Pipeline created successfully', pipeline_id, timestamp)
            
        elif pipeline_option == 'upk':
            if confirm_id(pipeline_id):
                if pipeline_key != confirm_key(pipeline_id):
                    return Response.error('Wrong key', pipeline_id, timestamp)
                
                if pipeline_new_key:
                    update_key(pipeline_id, pipeline_new_key)
                    return Response.success('Key updated successfully', pipeline_id, timestamp)
            else:
                return Response.error('ID not found', pipeline_id, timestamp)
        
        elif pipeline_option == 'snd':
            if confirm_id(pipeline_id):
                if pipeline_key != confirm_key(pipeline_id):
                    return Response.error('Wrong key', pipeline_id, timestamp)
                
                int_data: dict[str, int] = {}
                str_data: dict[str, str] = {}
                
                # Populate int_data
                for i in range(1, 9):
                    key = f'ivp{i}'
                    value = request.args.get(key)
                    if value:
                        if not value.isdigit() or int(value) > 9999:
                            return Response.error(f'Integer limit 4 digits for {key}', pipeline_id, timestamp)
                        int_data[key] = int(value)

                # Populate str_data
                for i in range(1, 5):
                    key = f'svp{i}'
                    value = request.args.get(key)
                    if value:
                        if len(value) > 128:
                            return Response.error(f'String limit 128 characters for {key}', pipeline_id, timestamp)
                        str_data[key] = value
                        
                # Check if the number of ivd values exceeds the limit
                if len(int_data) > 8:
                    return Response.error('Exceeded limit of 8 ivp values', pipeline_id, timestamp)
                
                # Check if the number of svd values exceeds the limit
                if len(str_data) > 4:
                    return Response.error('Exceeded limit of 4 svp values', pipeline_id, timestamp)

                if int_data or str_data:
                    data = {'int_virtual_pin': int_data, 'str_virtual_pin': str_data}
                    store_data(pipeline_id, data)
                    return Response.success('Data sent successfully', pipeline_id, timestamp)
                else:
                    return Response.error('Data not sent', pipeline_id, timestamp)
            else:
                return Response.error('ID not found', pipeline_id, timestamp)
        
        elif pipeline_option == 'rcv':
            if confirm_id(pipeline_id):
                if pipeline_key != confirm_key(pipeline_id):
                    return Response.error('Wrong key', pipeline_id, timestamp)
                
                if data_available(pipeline_id):
                    data = read_data(pipeline_id)
                    return Response.success('Data received successfully', pipeline_id, timestamp, {'stream': data})
                else:
                    return Response.error('Data not received', pipeline_id, timestamp)
            else:
                return Response.error('ID not found', pipeline_id, timestamp)
                       
        else: 
            return Response.error('Invalid request', pipeline_id, timestamp)
        
    except Exception as e:
        return Response.error(f'Internal server error: {str(e)}', pipeline_id, timestamp)

# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    timestamp = datetime.now().isoformat()
    return Response.error('Invalid request', '', timestamp)

# Main
if __name__ == '__main__':
    app.run()  # Run the app
    #app.run(debug=True)  # debug in production