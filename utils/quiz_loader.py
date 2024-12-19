import json
import config

def load_quiz_data():
    with open(config.DICT_DATA, 'r', encoding='utf-8') as j:
        return json.loads(j.read())
