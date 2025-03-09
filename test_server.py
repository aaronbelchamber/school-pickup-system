from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import datetime
import os

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            request_json = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            request_json = {"raw_data": post_data.decode('utf-8')} # capture non json posts.

        timestamp = datetime.datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "request": request_json
        }

        self.log_request(log_entry)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "received"}).encode('utf-8'))

    def log_request(self, log_entry):
        log_file = "request_log.json"
        log_data = []

        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                pass # if file doesnt exist or is corrupt, start fresh

        log_data.append(log_entry)

        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=4)

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()