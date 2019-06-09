import json

data = {}

def test_cases(filepath = 'vectors.json'):

    data_dict = {}

    with open(filepath) as json_file:
        data_dict = json.load(json_file)

    data_list = data_dict["english"]
    test_list = []

    for data in data_list:
        sequence_hex, mnemonic_string = data[0], data[1]
        r = bytes.fromhex(sequence_hex)
        s = mnemonic_string.split(" ")
        test_list.append((r, s))

    return test_list
