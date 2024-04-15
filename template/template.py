import json, requests

API_KEY = "YOUR_API_KEY"

template_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

translation_data = {
    0: "_",
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

def convert(message, starting_row):
    words = message.split()
    print(words)
    
    row = starting_row  # Starting row
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
            if char.upper() in translation_data.values():
                for key, value in translation_data.items():
                    if value == char.upper():
                        template_data[row][col + 1] = key
                        col += 1
                        break
            elif char == ' ':  # Check for space
                template_data[row][col + 1] = 0  # Assign 0 for space
                col += 1

        # Move to the next line if the word ended prematurely
        if col < 20:
            col += 1

    # Reset column and move to the next row for the next word
    row += 1
    col = 0
    
    return template_data

def send_post(data):
    # Making our POST
    url = "http://192.168.68.66:7000/local-api/message"

    headers = {
        "X-Vestaboard-Local-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }

    post_data = json.dumps(data)
    response = requests.post(url, headers=headers, data=post_data)
    print(response)

if __name__ == "__main__":
    message = "What You Want Your Message To Be"
    converted_data = convert(message, 1)
    send_post(converted_data)
