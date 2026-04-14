"""Static server for the frontend. Tries several ports — avoids blocked ports like 3000 on some Windows setups."""
import http.server
import os
import socketserver

PORTS = (8765, 8080, 5500, 9000, 3456)


def main() -> None:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    handler = http.server.SimpleHTTPRequestHandler
    last_err: OSError | None = None
    for port in PORTS:
        try:
            with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
                print(f"Serving frontend at http://127.0.0.1:{port}/")
                print(f"Open http://127.0.0.1:{port}/verify.html")
                httpd.serve_forever()
        except OSError as e:
            last_err = e
    raise SystemExit(f"Could not bind to any of {PORTS}: {last_err}")


if __name__ == "__main__":
    main()
