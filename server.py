#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Barqawi Archive — Public Website Server
Serves the read-only public archive for Railway deployment.
"""

import os
import json
import mimetypes
import http.server
from pathlib import Path

PORT = int(os.environ.get("PORT", 8080))
BASE = Path(__file__).parent


class Handler(http.server.BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {args[0]} {args[1]}")

    def do_GET(self):
        path = self.path.split("?")[0]

        # Articles JSON
        if path == "/articles.json":
            self._serve_file(BASE / "articles.json", "application/json")
            return

        # Images
        if path.startswith("/images/"):
            filename = os.path.basename(path[8:])
            self._serve_file(BASE / "images" / filename)
            return

        # Root → index.html
        if path == "/" or path == "":
            self._serve_file(BASE / "index.html", "text/html; charset=utf-8")
            return

        # Any other static file
        filepath = BASE / path.lstrip("/")
        if filepath.exists() and filepath.is_file():
            self._serve_file(filepath)
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Not found")

    def _serve_file(self, path, content_type=None):
        path = Path(path)
        if not path.exists():
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return
        if content_type is None:
            content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"\n  Barqawi Archive — Public Site")
    print(f"  Running on port {PORT}\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.")
