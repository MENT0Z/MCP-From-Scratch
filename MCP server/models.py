from dataclasses import dataclass
from typing import Any

@dataclass
class JsonRPCRequest:
    jsonrpc: str
    id: int|str
    method: str
    params : dict[str, Any]


@dataclass
class JsonRPCResponse:
    jsonrpc: str = "2.0"
    id: int|str|None = None
    result: Any = None
    error : Any = None