import os
import json

from flask import Flask, jsonify, request


# Variables
app = Flask(__name__)

folder_location: str = './pipeline'


# Functions
def make_folder_location(pipeline_id):
    parent_folder = './pipeline'
    folder_location = os.path.join(parent_folder, pipeline_id)
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)
    if not os.path.isdir(folder_location):
        os.mkdir(folder_location)
        
def confirm_folder_location(pipeline_id):
    if os.path.isdir(folder_location, pipeline_id):
        return True
    else:
        return False

def data_available(id: str) -> bool:
    with open(f'/pipeline/{id}/stream.json', 'w') as f:
        if f:
            return True
        else:
            return False

def store_data(id: str, data: dict) -> None:
    with open(f'/pipeline/{id}/stream.json', 'w') as f:
        json.dump(data, f)
        
def read_data(id: str) -> dict:
    with open(f'/pipeline/{id}/stream.json', 'r') as f:
        return json.load(f)
    

# Routes
@app.route('/')
def home():
    return "Welcome to Pair-Pipeline!"

@app.route('/pipeline/snd', methods=['POST'])
def pipeline_snd():
    pipeline_id: str = request.args.getlist('id')
    int_virtual_data: dict[str, list[int]] = {}
    str_virtual_data: dict[str, list[str]] = {}

    # Populate int_virtual_data
    for i in range(1, 17):
        key = f'ivd{i}'
        values = request.args.getlist(key)
        if values:
            int_virtual_data[key] = [int(ivd) for ivd in values]

    # Populate str_virtual_data
    for i in range(1, 5):
        key = f'svd{i}'
        values = request.args.getlist(key)
        if values:
            str_virtual_data[key] = [str(svd) for svd in values]
            
    if 
                      
    for x in int_virtual_data:
        int_count: int = 4
        if len(int_virtual_data[x]) > int_count:
            response = {'error': f'integer limit {int_count} values for {x}'}
            return jsonify(response), 400
        
    for x in str_virtual_data:
        str_count: int = 256
        if len(str_virtual_data[x]) > str_count:
            response = {'error': f'string limit {str_count} values for {x}'}
            return jsonify(response), 400

    if_folder_available = confirm_folder_location(pipeline_id)
    
    if if_folder_available == True:
        if int_virtual_data and str_virtual_data:
            store_data(pipeline_id, {**int_virtual_data, **str_virtual_data})
            response = {'message': 'Data stored successfully'}
        else:
            response = {'error': 'Data not stored'}
        
    else: 
        response = {'error': 'ID not available'}

    return jsonify(response), 201


@app.route('/pipeline/rcv', methods=['GET'])
def pipeline_receive():
    pipeline_id: str = request.args.getlist('id') 
    if_folder_available = confirm_folder_location(pipeline_id)
    
    if if_folder_available == True:
        data = read_data(pipeline_id)
        response = {'message': 'Data retrieved successfully', 'stream': data}
    else:
        response = {'error': 'Data not retrieved'}
    
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)