import json

"""
#
# Save dictionary to JSON file
#
"""
def save_dictionary_to_json(dictionary, json_file):
    print("Saving {} results file to {}".format(str(len(dictionary)), json_file))
    with open(json_file, 'w') as save:
        json.dump(dictionary, save)

"""
#
# Load dictionary from JSON file
#
"""
def load_dictionary_from_json(json_file):
    dictdump = {}
    print("Loading file from ", json_file)

    with open(json_file) as handle:
        dictdump = json.loads(handle.read())
    return dictdump