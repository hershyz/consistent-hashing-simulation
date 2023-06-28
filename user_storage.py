import random
import string

uuid_length = 64
uuids = []

# generate random uuid
def generate_random_uuid(length):
    characters = string.ascii_letters + string.digits
    random_uuid = ''.join(random.choice(characters) for _ in range(length))
    return random_uuid

# get numbers from uuid (for request routing to distinct server request handling thresholds)
def get_uuid_nums(uuid):
    res = ''
    for c in uuid:
        if c in string.digits:
            res += c            
    if res == '': return 0 # rare edge case -- all 64 characters are chosen from 'string.ascii_letters'
    return int(res)

# handle adding users
def add_users(n):
    for i in range(n):
        uuids.append(generate_random_uuid(uuid_length))

# handle removing users
def remove_users(n):
    for i in range(n):
        removal_index = random.randrange(len(uuids))
        uuids.pop(removal_index)