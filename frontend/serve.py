"""Static server for local-only dev when the API runs on another port (e.g. 8000). Serves `public/`."""
import http.server
import os
import socketserver
from pathlib import Path

PORTS = (8765, 8080, 5500, 9000, 3456)


def main() -> None:
    public = Path(__file__).resolve().parent.parent / "public"
    os.chdir(public)
    handler = http.server.SimpleHTTPRequestHandler
    last_err: OSError | None = None
    for port in PORTS:
        try:
            with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
                print(f"Serving frontend at http://127.0.0.1:{port}/")
                print(f"Open http://127.0.0.1:{port}/ (API must run on :8000)")
                httpd.serve_forever()
        except OSError as e:
            last_err = e
    raise SystemExit(f"Could not bind to any of {PORTS}: {last_err}")


if __name__ == "__main__":
    main()
