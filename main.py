# This is a GitHub Test of parsing FIX data using a json file

import json
import argparse
import sys


# loads the json formatting file
def load_json(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)


# loads the FIX file
def load_fix_log(fix_file):
    with open(fix_file, 'r') as f:
        return f.read()


# parse a single FIX message string into a dictionary using the tags
def parse_fix_message(message, tags):
    # split the message into fields using the '|' operator
    fields = message.split('|')
    parsed_message = {}
    # check if field contains tag and a value separated by exactly 1 '=' sign
    for field in fields:
        field.strip()
        if not field:
            continue
        if '=' not in field:
            print(field)
            print("element does not contain an '='")
            sys.exit()
        if field.count('=') > 1:
            print(field)
            print("element contains more than one '='")
            sys.exit()
        if '=' in field:
            tag, value = field.split('=')
            tag = tag.strip()
            value = value.strip()
            # pull the name for the tag
            tag_name = tags.get(tag, {}).get('name', tag)
            # check for enum
            if tags.get(tag, {}).get('type') == 'enum':
                # if so use .get to replace value
                value = tags[tag]['values'].get(value, value)
            parsed_message[tag_name] = value
    return parsed_message


# print each parsed message in json format
def print_parsed_messages(parsed_messages):
    for message in parsed_messages:
        print(json.dumps(message, indent=4))


# added new order count
def count_new_orders(parsed_messages):
    count = 0
    for msg in parsed_messages:
        if msg.get('MsgType') == 'NewOrderSingle':
            count += 1
    return count


# added accepted order count
def count_accepted_orders(parsed_messages):
    count = 0
    for msg in parsed_messages:
        if msg.get('ExecType') == 'New':
            count += 1
    return count


# main function to load files, parse FIX message and print results
def main():
    # set up argument parser for command-line inputs
    parser = argparse.ArgumentParser(description='Parse and print FIX messages.')
    # add option for part2 - q1
    parser.add_argument('command', choices=['part1', 'part2-q1', 'part2-q2'], help="select the part to run")
    # add CLI arg for FIX file
    parser.add_argument('-f', '--file', required=True, help='Path to the FIX log file.')
    # add CLI arg for json
    parser.add_argument('--tags', required=True, help='Path to the json tags file.')
    args = parser.parse_args()
    tags = load_json(args.tags)
    fix_log = load_fix_log(args.file)
    messages = fix_log.split('|8=')
    # added left messages[0]
    reconstructed = [messages[0]]
    parsed_messages = []
    # reconstructs messages
    for msg in messages[1:]:
        reconstructed.append("8=" + msg)
    # sends messages to parse_fix_message one at a time
    for msg in reconstructed:
        parsed_message = parse_fix_message(msg, tags)
        parsed_messages.append(parsed_message)

    if args.command == 'part2-q1':
        result = count_new_orders(parsed_messages)
        print(f"Number of new orders: {result}")
    elif args.command == 'part1':
        print_parsed_messages(parsed_messages)
    elif args.command == 'part2-q2':
        result = count_accepted_orders(parsed_messages)
        print(f"Number of accepted orders: {result}")


if __name__ == "__main__": main()
