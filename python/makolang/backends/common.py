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
    url: str # public
    method: str # public
    headers: Optional[dict[str, str]] # public
    payload: Optional[dict[str, Any]] # public
    
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
        self.code = code # public
        self.message = message # public
        self.response = response # public
        super().__init__(f'Upstream API error: {code} {message}')

__exports = [ 
    HTTPRequest,
    UpstreamAPIError,
    random_uuid
]