import json
# input file name should file path with extension
def removedup(Input_file): # Function remove the duplicate obj from json file
    unique_data = []
    with open(Input_file, 'r') as infile:
        data = json.load(infile)
        for item in data:
            if item not in unique_data:
                unique_data.append(item)
    with open("removeDups.json", "w") as writeJSON:
        json.dump(unique_data, writeJSON, ensure_ascii=False)

removedup("/Users/atulsmac/PycharmProjects/pythonBots/Isuzu2020-12-10.json")
