import json
from protocol import parse_request

class StdioTransport:
    def __init__(self, router):
        self.router = router

    def start(self):
        while True:
            raw = input()
            request = parse_request(raw)
            response = self.router.route(request)
            print(json.dumps(response.__dict__))