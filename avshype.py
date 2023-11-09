import requests
import json
import socket
import subprocess
import time
import logging
from datetime import datetime

# Configure logging
log_file_name = 'avshype.log'
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

# Function to check if the Colorado Avalanche is playing today
def is_colorado_avalanche_playing():
    current_date = datetime.now().strftime("%Y-%m-%d")
    endpoint = f"https://api-web.nhle.com/v1/schedule/{current_date}"
    response = requests.get(endpoint)

    if response.status_code == 200:
        schedule_data = response.json()

        for game_day in schedule_data.get("gameWeek", []):
            for game in game_day.get("games", []):
                home_team_id = game.get("homeTeam", {}).get("id")
                away_team_id = game.get("awayTeam", {}).get("id")

                if home_team_id == 21 or away_team_id == 21:
                    return True

        return False
    else:
        return False

# Check if the Colorado Avalanche is playing
if is_colorado_avalanche_playing():
    logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [INFO]: The Colorado Avalanche are playing today.")

    # Execute the first script
    send_razer_command("uwABsQEK")

    # Execute the second script

    send_razer_command("uwAgsAAKAAD//wAAAAD//wAAAAD/AAD//wAAAAD//wAAAAD/IQ==")

    # Run the third script in a loop for the specified duration
    total_duration = 8 * 60 * 60  # 8 hours
    interval = 30  # 30 seconds
    num_iterations = total_duration // interval

    for _ in range(num_iterations):
        send_message()
        time.sleep(interval)

    logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [INFO]: Script executed successfully.")
else:
    logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [INFO]: The Colorado Avalanche are not playing today.")
