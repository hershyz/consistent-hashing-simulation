import random
import server
import user_storage

# start with a single server - enforce request handling threshold of 3 significant digits
curr_server_id = 0
max_threshold = 1000
server_ring = [server.Server(server_id=curr_server_id, request_handling_threshold=max_threshold)]

# also initialze a single uuid inside of user storage
user_storage.uuids.append(user_storage.generate_random_uuid(user_storage.uuid_length))

# display server ring - for debugging purposes
def display_server_ring():
    print('Server ID | Request Handling Threshold')
    for s in server_ring:
        print([s.server_id, s.request_handling_threshold])

# handle adding servers
def add_servers(n):
    global curr_server_id
    for i in range(n):
        curr_server_id += 1
        insertion_index = random.randrange(len(server_ring))

        # if the insertion index is at the beginning (average between 0 and the existing first element)
        if insertion_index == 0:
            request_handling_threshold = int(server_ring[0].request_handling_threshold / 2)
            server_ring.insert(insertion_index, server.Server(server_id=curr_server_id, request_handling_threshold=request_handling_threshold))

        # otherwise, take the average of the element at the starting index and the element before it
        else:
            request_handling_threshold = int((server_ring[insertion_index].request_handling_threshold + server_ring[insertion_index - 1].request_handling_threshold) / 2)
            server_ring.insert(insertion_index, server.Server(server_id=curr_server_id, request_handling_threshold=request_handling_threshold))

# handle removing servers
def remove_servers(n):
    for i in range(n):
        removal_index = random.randrange(len(server_ring))
        server_ring.pop(removal_index)

# route requests
def route_requests():

    for s in server_ring: s.clients.clear() # clear all server client sets between simulations

    for uuid in user_storage.uuids:

        uuid_nums = user_storage.get_uuid_nums(uuid) # strip numbers from uuid for routing

        # find the first server with a request handling threshold >= the integer stored in 'uuid_nums' mod in the max server range
        for s in server_ring:
            if s.request_handling_threshold >= uuid_nums % max_threshold:
                s.clients.add(uuid)
                break