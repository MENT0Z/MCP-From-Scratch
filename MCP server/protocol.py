import json

from models import JsonRPCRequest

def parse_request(raw_request: str) -> JsonRPCRequest:
    """
    Parse a raw JSON-RPC request string into a JsonRPCRequest object.

    Args:
        raw_request (str): The raw JSON-RPC request string.

    Returns:
        JsonRPCRequest: The parsed JsonRPCRequest object.

    Raises:
        ValueError: If the raw request is not a valid JSON-RPC request.
    """

    request_dict = json.loads(raw_request)
    if request_dict["jsonrpc"] != "2.0":
        raise Exception("Invalid JSON-RPC version. Expected '2.0'.")
    return JsonRPCRequest(
        jsonrpc=request_dict["jsonrpc"],
        id=request_dict["id"],
        method=request_dict["method"],
        params=request_dict.get("params", {})
    )