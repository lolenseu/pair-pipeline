import os

parent_folder: str = '/pipeline/'

def make_folder_location(pipeline_id):
    parent_folder = './pipeline'
    folder_location = os.path.join(parent_folder, pipeline_id)
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)
    if not os.path.isdir(folder_location):
        os.mkdir(folder_location)

make_folder_location('12345678')
        
        
        