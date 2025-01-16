#!/usr/bin/python3

# Quick script to connect to Shodan's API and get info about a list of IPs in a file provided

import shodan
import argparse
import logging

# Set up command line arguments
parser = argparse.ArgumentParser(description='Query Shodan for information about services running on a list of IPs.')
parser.add_argument('-f', '--file', required=True, help='File containing the list of IPs')
parser.add_argument('-k', '--key', required=True, help='Shodan API key')
parser.add_argument('--debug', action='store_true', help='Enable debugging output')
args = parser.parse_args()

# Set up logging
if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# Read the list of IPs from the file
with open(args.file, 'r') as file:
    ip_list = [line.strip() for line in file]

# Initialize the Shodan API
api = shodan.Shodan(args.key)

for ip in ip_list:
    try:
        logging.debug(f"Querying Shodan for IP: {ip}")
        # Query Shodan for the IP
        host = api.host(ip)
        logging.debug(f"Received data for IP: {ip}")
        print(f"Information for IP: {ip}")
        print(f"Organization: {host.get('org', 'n/a')}")
        print(f"Operating System: {host.get('os', 'n/a')}")
        for item in host['data']:
            print(f"Port: {item['port']}")
            print(f"Service: {item.get('product', 'n/a')}")
            print(f"Banner: {item['data']}\n")
    except shodan.APIError as e:
        logging.error(f"Error querying Shodan for IP {ip}: {e}")
        print(f"Error: {e}")
