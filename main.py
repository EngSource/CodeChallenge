#This is a Github Test of loading the json file

import json
import argparse

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

#added new order count
def count_new_orders(parsed_messages):
    count = 0
    for msg in parsed_messages:
        if msg.get('MsgType') == 'NewOrderSingle':
            count += 1
    return count

#added accepted order count
def count_accepted_orders(parsed_messages):
    count = 0
    for msg in parsed_messages:
        if msg.get('ExecType') == 'New':
            count += 1
    return count



#main function to load files, parse FIX message and print results
def main():
    #set up argument parser for command-line inputs
    parser = argparse.ArgumentParser(description='Parse and print FIX messages.')
    #add option for part2 - q1
    parser.add_argument('command', choices=['part2-q1', 'part2-q2'], help="part2-q1 is available")
    #add CLI arg for FIX file
    parser.add_argument('-f', '--file', required=True, help='Path to the FIX log file.')
    #add CLI arg for json
    parser.add_argument('--tags', required=True, help='Path to the json tags file.')
    args = parser.parse_args()
    tags = load_json(args.tags)
    fix_log = load_fix_log(args.file)
    messages = fix_log.split('|8=')
    parsed_messages = []
    for msg in messages[1:]:
        parsed_message = parse_fix_message('8=' + msg, tags)
        parsed_messages.append(parsed_message)

    if args.command == 'part2-q1':
        result = count_new_orders(parsed_messages)
        print(f"Number of new orders: {result}")
    elif args.command == 'part2-q2':
        result = count_accepted_orders(parsed_messages)
        print(f"Number of accepted orders: {result}")



if __name__ == "__main__": main()

