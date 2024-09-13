#This is a Github Test of loading the json file

import json


#loads the json formatting file
def load_json(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

#loads the FIX file
def load_fix_log(fix_file):
    with open(fix_file, 'r') as f:
        return f.read()

#parse a single FIX message string into a dictionary using the tags
def parse_fix_message(message, tags):
    #split the message into fields using the '|' operator
    fields = message.split('|')
    parsed_message = {}
    #check if field contains tag and a value
    for field in fields:
        if '=' in field:
            tag, value = field.split('=')
            tag = tag.strip()
            value = value.strip()
            #pull the name for the tag
            tag_name = tags.get(tag, {}).get('name', tag)
            #check for enum
            if tags.get(tag, {}).get('type') == 'enum':
                #if so add parsed tag name to the dictionary
                value = tags[tag]['values'].get(value, value)
            parsed_message[tag_name] = value
    return parsed_message

#print each parsed message in json format
def print_parsed_messages(parsed_messages):
    for message in parsed_messages:
        print(json.dumps(message, indent=4))

#main function to load files, parse FIX message and print results
def main():
    #path locations
    tags_file = 'tags.json'
    fix_file = 'fix.log'
    #load tag definitions from json file
    tags = load_json(tags_file)
    #load data from FIX file
    fix_log = load_fix_log(fix_file)
    #parse each message and store it in a list
    messages = fix_log.split('|8=')
    parsed_messages = [parse_fix_message('8=' + msg, tags) for msg in messages[1:]]
    #print parsed messages in formatted json output
    print_parsed_messages(parsed_messages)


if __name__ == "__main__": main()