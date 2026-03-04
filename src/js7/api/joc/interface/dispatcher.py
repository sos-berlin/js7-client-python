from typing import Optional, Union, get_args, get_origin
from pydantic import BaseModel

from .resolver import Resolver
from ....model.private.api.endpoint import EndpointCall, EndpointDefinition


class Dispatcher(Resolver):
    def __init__(self, version: Optional[str]):
        super().__init__()
        self._version = version

    def set_version(self, version: str):
        self._version = version
    
    def dispatch(self, *, endpoint_id: str, call: EndpointCall) -> Union[BaseModel, bytes, bytearray]:
        # Auto discovery if no version is set.
        if not self._version:
            for ep in self._endpoint_cache:
                if endpoint_id == ep.id:
                    try:
                        return self._execute(ep, call)
                    except RuntimeError:
                        continue
            
            raise RuntimeError("Auto discovery for endpoint failed.")
        
        ep = self.resolve(version=self._version, endpoint_id=endpoint_id)
        
        return self._execute(ep, call)

    def _execute(self, endpoint_definition: EndpointDefinition, call: EndpointCall):
        # Validates payload
        if endpoint_definition.payload_model:
            if not call.payload:
                raise ValueError("Payload is required for this endpoint")
            if not isinstance(call.payload, endpoint_definition.payload_model):
                raise TypeError(
                    f"Payload must be {endpoint_definition.payload_model.__name__}"
                )

        # Validates options
        if endpoint_definition.options:
            call_options = call.options or {}

            for name, typ in endpoint_definition.options.items():
                value = call_options.get(name)

                # Optional[T]
                if get_origin(typ) is Union and type(None) in get_args(typ):
                    inner = next(t for t in get_args(typ) if t is not type(None))
                    if value is not None and not isinstance(value, inner):
                        raise TypeError(
                            f"Option '{name}' must be {inner.__name__} or None"
                        )
                    continue

                # Required option
                if value is None:
                    raise ValueError(f"Missing option '{name}'")

                if not isinstance(value, typ):
                    raise TypeError(
                        f"Option '{name}' must be {typ.__name__}"
                    )

        # Calls the endpoint function from 'EndpointDefinition'
        result = endpoint_definition.function(call)

        # Validate response type        
        if not isinstance(result, endpoint_definition.response_model):
            raise TypeError(
                f"Invalid response type: expected {endpoint_definition.response_model.__name__}"
            )

        return result