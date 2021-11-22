import json
import random
import time

from http.server import BaseHTTPRequestHandler
from routes.main import routes
from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler
from response.sensorHandler import SensorHandler
from response.stringHandler import StringResponseHandler
from datetime import datetime
from urllib.parse import urlparse
from urllib.parse import parse_qs


class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_POST(self):
        if self.path == "/update-settings":
            handler = StringResponseHandler()
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            handler.set_response(str(post_body))
            handler.setStatus(200)
            print("update-settings")
        elif self.path == "/reboot":
            handler = StringResponseHandler()
            handler.set_response(str("Module rebooting"))
            handler.setStatus(200)
        else:
            handler = StringResponseHandler()
            handler.set_response("Unknown route")
            handler.setStatus(404)
        self.respond({
            'handler': handler
        })

    def do_GET(self):
        if self.path == "/":
            handler = StaticHandler()
            handler.find("/index.html")
        elif self.path.startswith("/sensor?"):
            query = urlparse(self.path).query
            parameters = parse_qs(query)
            handler = SensorHandler()
            handler.get_data(parameters)
        elif self.path == "/heapfree":
            handler = StringResponseHandler()
            handler.set_response(str(random.randint(20000, 40000)))
        elif self.path == "/time":
            handler = StringResponseHandler()
            handler.set_response(datetime.now().replace(microsecond=0).isoformat())
        elif self.path == "/status":
            handler = StringResponseHandler()
            status = {}
            status["dt"] = datetime.now().replace(microsecond=0).isoformat()
            status["te"] = str(random.randint(0, 200) / 10)
            status["ws"] = str(random.randint(0, 1000) / 10)
            status["wd"] = str(random.randint(0, 359))
            status["rh"] = str(random.randint(0, 1000) / 10)
            status["bp"] = str(random.randint(9800, 11000) / 10)
            json_msg = json.dumps(status)
            handler.set_response(json_msg)
        elif self.path == "/reboot":
            handler = StringResponseHandler()
            handler.set_response("Module rebooting")
        elif self.path == "/read-settings":
            handler = StringResponseHandler()
            handler.set_response(
                '{"ssid":"Casa de Lima","ipaddr":"192.168.1.100","gatewayaddr":"192.168.1.250","proxyaddr":"192.168.1.130","utcoffset":"720"}')
        else:
            # Static files in public folder
            handler = StaticHandler()
            handler.find(self.path)
        self.respond({
            'handler': handler
        })

    def handle_http(self, handler):
        status_code = handler.getStatus()
        # time.sleep(0.5)
        self.send_response(status_code)

        if status_code is 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = "404 Not Found"

        self.end_headers()

        if isinstance(content, bytes):
            return content
        else:
            return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)
