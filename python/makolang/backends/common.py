from typing import NamedTuple, Any, Optional
from uuid import uuid4

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

def random_uuid() -> str:
    """
    生成随机 UUID。
    
    :return: UUID
    """
    return str(uuid4())

class HTTPRequest(NamedTuple):
    url: str
    method: str
    headers: Optional[dict[str, str]]
    payload: Optional[dict[str, Any]]
    
    def request(self):
        import requests
        return requests.request(
            self.method,
            self.url,
            headers=self.headers,
            json=self.payload
        )
    
    def save(self, path: str):
        with open(path, 'wb') as f:
            f.write(self.request().content)
    
class UpstreamAPIError(Exception):
    def __init__(self, code: str, message: str|None, response: str|None) -> None:
        self.code = code
        self.message = message
        self.response = response
        super().__init__(f'Upstream API error: {code} {message}')

__exports = [ 
    HTTPRequest,
    UpstreamAPIError,
    random_uuid
]