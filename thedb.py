import json
import os
import random

def _load_aphorisms(f):
    json_arr = json.loads(open(_json_file).read())
    aphorisms = dict((item["slug"], item) for item in json_arr)
    return aphorisms

def get(slug):
    return _aphorisms.get(slug)

def get_random(count):
    keys = random.sample(_aphorisms, min(count, len(_aphorisms)))
    return [_aphorisms[key] for key in keys]

_json_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "aphorisms.json")
_aphorisms = _load_aphorisms(_json_file)

if __name__ == '__main__':
    print _aphorisms



