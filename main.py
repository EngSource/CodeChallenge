#This is a Github Test of loading the json file

import json

#loads the json formatting file
def load_json_file(formatting_file):
    with open(formatting_file, 'r') as json_file:
        return json.load(json_file)

#loads the FIX file and splits it into packets
def load_fix_file(data_file):
    with open(data_file, 'r') as fix_file:
        return fix_file.read().splitlines()


#Reference local json file
json_file_path = "tags.json"

#prints json file
#print(load_json_file(json_file_path))

#Reference local fix data file
fix_file_path = "fix.log"

log = load_fix_file(fix_file_path)

packets = [packet.split('|') for packet in log]

print(packets)