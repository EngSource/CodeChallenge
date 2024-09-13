#This is a Github Test of loading the json file

import json

#loads the json formatting file
def load_file(formatting_file):
    with open(formatting_file, 'r') as f:
        return json.load(f)

#Use raw string
json_file_path = r"C:\Users\jwroi\Downloads\imandra-technical-interview-1.0.2\data\tags.json"

#prints json file
#print(load_file(json_file_path))