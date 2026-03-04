from typing import Any, Callable, Dict, Mapping, Optional, Tuple, Type, Union
from pydantic import BaseModel
from dataclasses import dataclass
from pydantic import BaseModel

from ....service.http_service import HTTPService


@dataclass
class EndpointCall:
    """Defines the endpoint of an internal API call."""
    
    http_service: HTTPService
    access_token: Optional[str] = None
    payload:      Optional[Union[BaseModel, bytes, Dict[str, Any]]] = None
    options:      Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class EndpointDefinition:
    """Definition for API endpoint function."""

    id:              str
    function:        Callable[[EndpointCall], Union[BaseModel, bytes, bytearray]]
    version:         Tuple[str, str] # e. g. from: "2.8.2" to: "3.1.0"
    response_model:  Union[Type[BaseModel], Type[bytes], Type[bytearray]]
    payload_model:   Optional[Union[Type[BaseModel], Type[bytes], Type[Dict[str, Any]]]] = None
    options:         Optional[Mapping[str, Type[Any]]] = None
    
    
