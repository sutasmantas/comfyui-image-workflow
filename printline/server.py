from __future__ import annotations

import argparse
import json
import mimetypes
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .service import JobNotFound, JobService
from .workflow import ValidationError


MAX_BODY_BYTES = 32_768
OUTPUT_NAME = re.compile(r"^[a-f0-9]{32}\.(?:svg|png|jpg|webp)$")


class PrintlineServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], root: Path, service: JobService | None = None):
        self.root = root
        self.service = service or JobService(root)
        super().__init__(address, PrintlineHandler)

    def server_close(self) -> None:
        self.service.close()
        super().server_close()


class PrintlineHandler(BaseHTTPRequestHandler):
    server: PrintlineServer

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/jobs":
            return self._json(HTTPStatus.OK, {"jobs": self.server.service.list()})
        if path.startswith("/api/jobs/"):
            job_id = path.removeprefix("/api/jobs/")
            try:
                return self._json(HTTPStatus.OK, self.server.service.get(job_id))
            except JobNotFound:
                return self._error(HTTPStatus.NOT_FOUND, "job_not_found", "Job was not found.")
        if path.startswith("/outputs/"):
            return self._output(path.removeprefix("/outputs/"))
        static = {"/": "index.html", "/app.js": "app.js", "/styles.css": "styles.css"}
        if path in static:
            return self._file(self.server.root / "static" / static[path])
        return self._error(HTTPStatus.NOT_FOUND, "not_found", "Route was not found.")

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            payload = self._body()
        except ValidationError as exc:
            return self._error(HTTPStatus.BAD_REQUEST, "invalid_json", str(exc))

        if path == "/api/jobs":
            try:
                job = self.server.service.create(payload)
                return self._json(HTTPStatus.ACCEPTED, job)
            except ValidationError as exc:
                return self._error(HTTPStatus.UNPROCESSABLE_ENTITY, "invalid_recipe", str(exc))

        retry_match = re.fullmatch(r"/api/jobs/([a-f0-9]{32})/retry", path)
        if retry_match:
            try:
                job = self.server.service.retry(retry_match.group(1))
                return self._json(HTTPStatus.ACCEPTED, job)
            except JobNotFound:
                return self._error(HTTPStatus.NOT_FOUND, "job_not_found", "Job was not found.")
            except ValueError as exc:
                return self._error(HTTPStatus.CONFLICT, "retry_not_allowed", str(exc))

        return self._error(HTTPStatus.NOT_FOUND, "not_found", "Route was not found.")

    def _body(self) -> Any:
        length = int(self.headers.get("Content-Length", "0"))
        if length > MAX_BODY_BYTES:
            raise ValidationError(f"Request body exceeds {MAX_BODY_BYTES} bytes.")
        try:
            return json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError as exc:
            raise ValidationError("Request body must contain valid JSON.") from exc

    def _json(self, status: HTTPStatus, payload: Any) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _error(self, status: HTTPStatus, code: str, message: str) -> None:
        self._json(status, {"error": {"code": code, "message": message}})

    def _file(self, path: Path) -> None:
        if not path.is_file():
            return self._error(HTTPStatus.NOT_FOUND, "not_found", "Asset was not found.")
        data = path.read_bytes()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _output(self, filename: str) -> None:
        if not OUTPUT_NAME.fullmatch(filename):
            return self._error(HTTPStatus.NOT_FOUND, "artifact_not_found", "Artifact was not found.")
        path = self.server.service.outputs / filename
        if not path.is_file():
            return self._error(HTTPStatus.NOT_FOUND, "artifact_not_found", "Artifact was not found.")
        return self._file(path)

    def log_message(self, format: str, *args: Any) -> None:
        print(f"{self.address_string()} - {format % args}")


def create_server(
    host: str = "127.0.0.1",
    port: int = 8042,
    *,
    root: Path | None = None,
    service: JobService | None = None,
) -> PrintlineServer:
    return PrintlineServer((host, port), root or Path(__file__).resolve().parents[1], service)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Printline workflow service.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8042, type=int)
    args = parser.parse_args()
    server = create_server(args.host, args.port)
    print(f"Printline listening on http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
