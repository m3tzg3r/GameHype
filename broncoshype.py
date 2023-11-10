#!/usr/bin/env python3

import requests
import json
import socket
import subprocess
import time
import logging
from datetime import datetime

# Configure logging
log_file_name = 'broncoshype.log'
logging.basicConfig(filename=log_file_name, level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def send_razer_command(pt):
    message = {"msg": {"cmd": "razer", "data": {"pt": pt}}}
    group = "239.255.255.250"
    port = 4001
    ttl = 2
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    json_result = json.dumps(message)
    logging.info(f"Sending: {json_result}")
    sock.sendto(bytes(json_result, "utf-8"), (group, port))

def send_message():
    message = {"msg": {"cmd": "status", "data": {}}}
    group = "239.255.255.250"
    port = 4001
    ttl = 2
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    json_result = json.dumps(message)
    logging.info(f"Sending: {json_result}")
    sock.sendto(bytes(json_result, "utf-8"), (group, port))

# Function to check if the Denver Broncos are playing today
def is_denver_broncos_playing(api_url):
    try:
        # Fetch data from the API endpoint
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse JSON response
        data = response.json()

        # Get the current date
        current_date = datetime.now().strftime('%Y-%m-%dT%H:%MZ')

        # Iterate through each event and compare the date with the current date
        for event in data.get('events', []):
            event_date = event.get('date', 'N/A')

            # Check if the event date is today
            if event_date == current_date:
                return True

        return False

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        return False

# Check if the Denver Broncos are playing
api_endpoint = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/7/schedule?season=2023"
if is_denver_broncos_playing(api_endpoint):
    logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [INFO]: The Denver Broncos are playing today.")

    # Execute the first script
    send_razer_command("uwABsQEK")

    # Execute the second script
    send_razer_command("uwAgsAAKAAD//30AAAD//30AAAD/AAD//30AAAD//30AAAD/IQ==")

    # Run the third script in a loop for the specified duration
    total_duration = 8 * 60 * 60  # 8 hours
    interval = 30  # 30 seconds
    num_iterations = total_duration // interval

    for _ in range(num_iterations):
        send_message()
        time.sleep(interval)

    logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [INFO]: Script executed successfully.")
else:
    logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [INFO]: The Denver Broncos are not playing today.")
