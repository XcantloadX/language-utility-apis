from enum import Enum
from typing import NamedTuple, Any, Callable, Optional
from dataclasses import dataclass

class Method(Enum):
    GET = 1
    POST = 2
    


class ActionRequest(NamedTuple):
    queries: dict[str, str]
    payload: str
    
class ActionResponse(NamedTuple):
    http_code: int
    data: dict[str, Any] | str
    headers: Optional[dict[str, str]]
    
    @classmethod
    def fail(cls, code: int, message: str, data: dict[str, Any]|None = None) -> 'ActionResponse':
        return cls(
            400, 
            { 'message': message, 'code': code },
            { 'Content-Type': 'application/json' }
        )
        
    @classmethod
    def success(cls, data: dict[str, Any]) -> 'ActionResponse':
        return cls(
            200,
            { 'message': 'ok', 'code': 0, 'data': data },
            { 'Content-Type': 'application/json' }
        )
        
    @classmethod
    def redirect(cls, url: str) -> 'ActionResponse':
        return cls(
            302,
            '',
            { 'Location': url }
        )

@dataclass
class Action:
    method: Method
    endpoint: str
    function: Callable[[ActionRequest], ActionResponse]

class GetAction(Action):
    def __init__(self, endpoint: str, function: Callable[[ActionRequest], ActionResponse]):
        super().__init__(Method.GET, endpoint, function)