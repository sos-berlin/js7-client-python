import importlib
import os
from pathlib import Path
from typing import List

from ....model.private.api.endpoint import EndpointDefinition

from ....util.check_matching_version import check_matching_version


class Resolver:
    def __init__(self):
        self._endpoint_cache: List[EndpointDefinition] = []
        self._load_endpoints(
            base_package="js7.api.joc.http",
            base_path = Path(__file__).parents[1] / "http"
        )

    def _load_endpoints(self, *, base_package: str, base_path: Path) -> None:
        """
        Walks through js7/api/joc/http and imports all modules
        that expose ENDPOINT_DEFINITION.
        """

        for root, _, files in os.walk(base_path):
            for file in files:
                if not file.endswith(".py"):
                    continue
                if file.startswith("__"):
                    continue

                file_path = Path(root) / file

                # relative path without .py
                rel_path = file_path.relative_to(base_path).with_suffix("")

                # module import path
                module_path = ".".join(
                    [base_package] + list(rel_path.parts)
                )

                module = importlib.import_module(module_path)

                if hasattr(module, "ENDPOINT_DEFINITION"):
                    endpoint_def = getattr(module, "ENDPOINT_DEFINITION")

                    if not isinstance(endpoint_def, EndpointDefinition):
                        raise TypeError(
                            f"{module_path}.ENDPOINT_DEFINITION is not EndpointDefinition"
                        )

                    self._endpoint_cache.append(endpoint_def)
        
    def resolve(self, *, version: str, endpoint_id: str) -> EndpointDefinition:
        """
        Resolves the endpoint definition for a given JOC version.
        """
        
        if not self._endpoint_cache:
            raise RuntimeError("Endpoint cache is empty.")
        
        for ep in self._endpoint_cache:
            ep_min_version, ep_max_version = ep.version
            
            version_is_ok = check_matching_version(
                min=ep_min_version, 
                max=ep_max_version, 
                check=version
            )
            
            if endpoint_id == ep.id and version_is_ok:
                return ep
        
        raise ValueError(f"Endpoint with id: {endpoint_id} and version {version} is not available.")    

