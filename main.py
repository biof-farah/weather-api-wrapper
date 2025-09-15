from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from weather_service import GetWeather
client = GetWeather()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != "/weather":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return
        
        params = parse_qs(parsed.query)
        city = params.get("city", ["Cairo"])[0]
        mode = params.get("mode", ["weather"])[0]

        try:
            if mode == "weather":
                result =  client.get_weather(city)
            elif mode == "forecast":
                result = client.get_forecast(city)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not Found")
                return
            
            body = json.dumps(result).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)


        except RuntimeError as e:
            retry_after = e.retry_after or "60"
            self.send_response(429)
            self.send_header("Retry-After", str(retry_after))
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error" : "rate_limited",
                "retry_after": retry_after
            }).encode())
        except Exception as exc:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "something went wrong, please try again"
            }).encode())



if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8000), Handler)
    print ("Server is running on http://localhost:8000")
    server.serve_forever()