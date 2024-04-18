import datetime
import requests
import json
import time
import schedule
import re
import sys
import os

def get_vestaboard_key():
    script_dir = os.path.dirname(__file__)
    key_file = os.path.join(script_dir, "VESTABOARD_KEY")
    if os.path.exists(key_file):
        with open(key_file, "r") as f:
            key = f.read().strip()
            return key
    else:
        print(f"Error: {key_file} not found.")
        return None

API_KEY = get_vestaboard_key()
BOARD_IP = "192.168.68.66"

run_time = "00:00"
debug = False

# Original data
original_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Data values mapping
data_values = {
    0: "Blank",
    1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J",
    11: "K", 12: "L", 13: "M", 14: "N", 15: "O", 16: "P", 17: "Q", 18: "R", 19: "S", 20: "T",
    21: "U", 22: "V", 23: "W", 24: "X", 25: "Y", 26: "Z",
    27: "1", 28: "2", 29: "3", 30: "4", 31: "5", 32: "6", 33: "7", 34: "8", 35: "9", 36: "0",
    37: "!", 38: "@", 39: "#", 40: "$", 41: "(", 42: ")",
    44: "-", 46: "+", 47: "&", 48: "=", 49: ";", 50: ":", 52: "'",
    53: '"', 54: "%", 55: ",", 56: ".", 59: "/", 60: "?",
    62: "|", 63: "Red", 64: "Orange", 65: "Yellow", 66: "Green", 67: "Blue", 68: "Violet",
    69: "White", 70: "Black", 71: "Filled"
}

def convert(message):
    words = message.split()
    
    row = 1  # Starting row
    col = 0  # Starting column

    # Assuming template_data is initialized and translation_data is defined elsewhere

    for word in words:
        # Check if adding the next word would cause it to overflow
        if col + len(word) > 20:
            row += 1
            col = 0

        for char in word:
            if col >= 20:
                row += 1
                col = 0
            if char.upper() in data_values.values():
                for key, value in data_values.items():
                    if value == char.upper():
                        original_data[row][col + 1] = key
                        col += 1
                        break
            elif char == ' ':  # Check for space
                original_data[row][col + 1] = 0  # Assign 0 for space
                col += 1

        # Move to the next line if the word ended prematurely
        if col < 20:
            col += 1

    # Reset column and move to the next row for the next word
    row += 1
    col = 0
            
def calculate_percent():
    global percent_of_year, now
    # Calculate the percentage of the year
    now = datetime.datetime.now()
    year_start = datetime.datetime(now.year, 1, 1)
    year_end = datetime.datetime(now.year + 1, 1, 1)
    current_time = now.timestamp()
    year_start_time = year_start.timestamp()
    year_end_time = year_end.timestamp()

    percent_of_year = round((current_time - year_start_time) / (year_end_time - year_start_time) * 100, 2)

def construct_message():
    calculate_percent()
    # Constructing the message
    message = f"We are {percent_of_year}% through {now.year}!"
    convert(message)

    # Determine how many sections to fill with "Filled" (representing filled sections)
    sections_to_fill = int(percent_of_year / 5)  # Because there are 20 sections and 100% / 20 = 5%

    # Fill in the values on line 5
    for i in range(20):
        if i < sections_to_fill:
            original_data[4][i+1] = 69  # White
        elif i == sections_to_fill:
            original_data[4][i+1] = 63  # Red
        else:
            original_data[4][i+1] = 0  # Blank

    return original_data

def send_post(data):
    if debug:
        print(data)
    else:
        # Making our POST
        url = f"http://{BOARD_IP}:7000/local-api/message"

        headers = {
            "X-Vestaboard-Local-Api-Key": API_KEY,
            "Content-Type": "application/json"
        }

        post_data = json.dumps(data)
        response = requests.post(url, headers=headers, data=post_data)
        print(response)

def job():
    while True:
        data = construct_message()
        print("Attempting to send message...")
        try:
            send_post(data)
            print("Message sent successfully.")
            break  # Exit the retry loop if sending is successful
        except Exception as e:
            print(f"Error occurred when sending POST request: {e}")
            print("Retrying in 60 seconds...")
            time.sleep(60)
            
def check_time_format(input_time):
    pattern = re.compile(r'^\d{2}:\d{2}$')  # Regular expression pattern for "HH:MM"
    return bool(pattern.match(input_time))

if __name__ == "__main__" and API_KEY is not None:
    can_run = False
    
    run_time = input("Enter time to run at as HH:MM. Ex 18:00 | ")
    if run_time == "ADMIN":
        print("Entering administration mode")
        print("Force running now...")
        job()
    elif run_time == "DEBUG":
        debug = True
        print("Entering debug mode")
        print("Force running now...")
        job()
    elif check_time_format(run_time):
        print("Input time is in the correct format.")
        can_run = True
    else:
        print("Input time is not in the correct format.")
        can_run = False
        sys.exit()
    
    if run_time and can_run == True:
        # Schedule the job to run every day at run_time
        schedule.every().day.at(run_time).do(job)
    
    print(f"Time set to run is {run_time}")
    
    print("Waiting to run job...")
    counter = 1
    if run_time != "DEBUG" and run_time != "ADMIN":
        while True:
            counter += 1
            if counter >= 60:
                print("Waiting to run job...")
                counter = 0
            # Run the scheduled jobs
            schedule.run_pending()
            time.sleep(1)  # Sleep for 1 second to avoid high CPU usage