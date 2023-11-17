#!/usr/bin/env python3

import requests
import json
import socket
import subprocess
import time
import logging
from datetime import datetime

# Configure logging
log_file_name = 'NuggetsHype.log'
logging.basicConfig(filename=log_file_name, level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def send_poweron():
    message = {"msg":{"cmd":"turn","data":{"value":1}}}
    group = "239.255.255.250"
    port = 4001
    ttl = 2
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    json_result = json.dumps(message)
    logging.info(f"Sending: {json_result}")
    sock.sendto(bytes(json_result, "utf-8"), (group, port))

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

def send_keepalive():
    message = {"msg": {"cmd": "status", "data": {}}}
    group = "239.255.255.250"
    port = 4001
    ttl = 2
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    json_result = json.dumps(message)
    logging.info(f"Sending: {json_result}")
    sock.sendto(bytes(json_result, "utf-8"), (group, port))

# Define the endpoint URL
endpoint_url = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"

# Send a GET request to the endpoint
response = requests.get(endpoint_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()

    # Check if API is current and gameDate matches current date.
    current_date = datetime.now().strftime('%Y-%m-%d')
    if data["scoreboard"]["gameDate"] == current_date:
        # Check if "DEN" is present in the output and indicate if the Denver Nuggets are playing
        if any("DEN" in game.get("gameCode", "") for game in data["scoreboard"]["games"]):
            for game in data["scoreboard"]["games"]:
                if "DEN" in game.get("gameCode", ""):
                    game_code = game.get("gameCode", "N/A")
                    logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [INFO]: The Denver Nuggets are playing today. Game Code: {game_code}")
                    
                    # Execute power on and sleep 5 seconds
                    send_poweron()
                    time.sleep(1)

                    # Execute the first script
                    send_razer_command("uwABsQEK")

                    # Execute the second script
                    send_razer_command("uwAgsAAKAAD///8AAAD///8AAAD/AAD///8AAAD///8AAAD/IQ==")

                    # Run the third script in a loop for the specified duration
                    total_duration = 4 * 60 * 60  # 4 hours
                    interval = 30  # 30 seconds
                    num_iterations = total_duration // interval

                    for _ in range(num_iterations):
                        send_keepalive()
                        time.sleep(interval)

            logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [INFO]: Script executed successfully.")
        else:
            logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [INFO]: Denver Nuggets are not playing today.")
    else:
        logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [INFO]: API not updated yet. Current date: {current_date}. Game date retrieved from API: {data['scoreboard']['gameDate']} :(")
else:
    logging.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [ERROR]: Failed to retrieve data from the endpoint.")
