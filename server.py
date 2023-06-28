class Server:

    def __init__(self, server_id, request_handling_threshold):
        self.server_id = server_id
        self.request_handling_threshold = request_handling_threshold
        self.clients = set() # better if we have O(1) lookup times here -- indexing isn't important