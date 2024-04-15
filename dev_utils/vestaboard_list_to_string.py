def translate_list(input_list, translation_data):
    translated_list = []
    for sublist in input_list:
        translated_sublist = []
        for num in sublist:
            if num in translation_data:
                translated_sublist.append(translation_data[num])
            else:
                translated_sublist.append("Unknown")
        translated_list.append(translated_sublist)
    return translated_list

# Translation data
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

# Input list
input_list = eval(input("Enter the list: "))

# Translate the list
translated_list = translate_list(input_list, translation_data)

# Print the translated list
for sublist in translated_list:
    print(sublist)
