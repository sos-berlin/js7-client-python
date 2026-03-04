import gzip
import mimetypes
from pathlib import Path
import http.client, ssl, time
from typing import Callable, Optional, Union, Dict
from ssl import SSLContext
import uuid

from ..model.configuration.http_configuration import HTTPConfiguration


class HTTPService:
    """
    Functionality:
    - Uses `time.monotonic` to obtain a monotonically increasing time source and
    avoid issues caused by system time changes (e.g. daylight saving time)
    - Closes the connection to the server after 30 seconds of inactivity and reopen the connection after the next use again.
    """
    
    IDLE_TIMEOUT = 30 # Reconnects after 30 seconds of inactivity
    
    def __init__(
        self, 
        *, 
        configuration: HTTPConfiguration,
        response_validator: Optional[Callable[[str, int, bytes], None]] = None
    ):
    
        self._config = configuration
        self._response_validator = response_validator
        
        self._conn: Union[http.client.HTTPSConnection, http.client.HTTPConnection, None] = None
        self._https_ctx: Optional[SSLContext] = None
        self._last_used: float = 0.0

        # These variables can be modified at runtime by other methods to adjust the SSL context
        self.auth_certfile_path: Optional[Union[Path, str]] = None
        self.auth_keyfile_path:  Optional[Union[Path, str]] = None
        
    def __enter__(self):
        self._ensure_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
        if exc_type is not None:
            self.close()

    def _ensure_connection(self):
        now = time.monotonic()
        if self._conn is None or (now - self._last_used) > self.IDLE_TIMEOUT:
            self._open_connection()
    
    # Creates the context for the ssl connection
    def _create_ssl_context(self) -> SSLContext:
        if self._https_ctx:
            return self._https_ctx
        
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

        # Sets fixed tls version
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        
        # Optional: Server Certificate
        if self._config.cafile_path:
            ctx.load_verify_locations(cafile=self._config.cafile_path)

        # Optional: Client certificate
        if self.auth_certfile_path and not self.auth_keyfile_path:
            raise ValueError("client certificate provided without private key")
        
        if self.auth_certfile_path and self.auth_keyfile_path:
            ctx.load_cert_chain(
                certfile=self.auth_certfile_path,
                keyfile=self.auth_keyfile_path
            )

        # Ensures security
        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.check_hostname = True
        self._https_ctx = ctx
        return self._https_ctx

    def _open_connection(self):
        self.close()
        
        if self._config.ssl:
            self._conn = http.client.HTTPSConnection(
                host=self._config.host,
                port=self._config.port,
                timeout=30,
                context=self._create_ssl_context()
            )
        else:
            self._conn = http.client.HTTPConnection(
                host=self._config.host, 
                port=self._config.port, 
                timeout=30
            )
        
        self._last_used = time.monotonic()

    def _request(self, method: str, path: str, headers: Dict[str, str], body: Optional[str]) -> http.client.HTTPResponse:
        self._ensure_connection()
        
        conn = self._conn
        if conn is None:
            raise RuntimeError("Connection not initialized.")
        
        response: Optional[http.client.HTTPResponse] = None
        
        # Reconnects and retries the request once on connection failure
        try:
            conn.request(method=method, url=path, body=body, headers=headers)
            response = conn.getresponse()
        except (BrokenPipeError, ConnectionResetError, TimeoutError):
            self.close()
            
            time.sleep(3) # Waits for 3 seconds
            
            self._open_connection()
            conn = self._conn
            if conn is None:
                raise RuntimeError("Connection not initialized after reconnect.")
            conn.request(method=method, url=path, body=body, headers=headers)
            response = conn.getresponse()
        
        return response
    
    def _decode_response(self, path:str, response: http.client.HTTPResponse) -> bytes:
        raw_bytes = response.read()
        
        # Raises a error for the given statuscode
        if self._response_validator:
            self._response_validator(path, response.status, raw_bytes)
        
        if "gzip" in (response.headers.get("Content-Encoding", "")).lower():
            return gzip.decompress(raw_bytes)
        
        return raw_bytes
    
    # (i) close method
    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None
            self._https_ctx = None
        
    # (i) POST method
    def post(self, path: str, body: Optional[str], headers: Dict[str, str]) -> bytes:
        response = self._request("POST", path, headers, body)
        return self._decode_response(path, response)
    
    # (i) GET method
    def get(self, path: str, headers: Dict[str, str]) -> bytes:
        response = self._request(method="GET", path=path, headers=headers, body=None)
        return self._decode_response(path, response)
    
    # (i) Upload file
    def upload_file(self, path: str, access_token: str, file: bytes, filename: str, form_fields: Optional[Dict[str, str]] = None) -> bytes:
        self._ensure_connection()
        conn = self._conn
        if conn is None:
            raise RuntimeError("Connection not initialized.")

        boundary = "----Boundary" + uuid.uuid4().hex
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

        body = bytearray()

        def add_field(name: str, value: str) -> None:
            body.extend(f"--{boundary}\r\n".encode())
            body.extend(
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
            )
            body.extend(value.encode("utf-8"))
            body.extend(b"\r\n")

        # optional form fields first
        if form_fields:
            for k, v in form_fields.items():
                add_field(k, v)

        # file part
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(
            (
                f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
                f"Content-Type: {content_type}\r\n\r\n"
            ).encode()
        )
        body.extend(file)
        body.extend(b"\r\n")

        # closing boundary
        body.extend(f"--{boundary}--\r\n".encode())

        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
            "X-Access-Token": access_token,
        }

        conn.request("POST", path, body=body, headers=headers)
        response = conn.getresponse()

        return self._decode_response(path=path, response=response)
