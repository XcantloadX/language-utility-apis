from typing import NamedTuple, Any

class HTTPRequest(NamedTuple):
    url: str
    method: str
    headers: dict[str, str]
    payload: dict[str, Any]