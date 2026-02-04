import os
import psutil
import shutil

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from common.common_utility import config

HOST = config["monitoring_agent"]["host"]
PORT = config["monitoring_agent"]["port"]


class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        def metric_collector():
            def bytes_to_megabytes(val):
                return round(val / (1024 * 1024) , 2)
            
            def bytes_to_gigabytes(val):
                return round(val / (1024 * 1024 * 1024), 2)
            
            response = {}

            response["b"] = {}
            response["b"]["memmory_total"] = psutil.virtual_memory().total
            response["b"]["memmory_used"] = psutil.virtual_memory().used
            response["b"]["memmory_free"] = psutil.virtual_memory().free
            response["b"]["disk_total"] = shutil.disk_usage("/").total
            response["b"]["disk_used"] = shutil.disk_usage("/").used
            response["b"]["disk_free"] = shutil.disk_usage("/").free

            response["mb"] = {}
            response["mb"]["memmory_total"] = bytes_to_megabytes(response["b"]["memmory_total"])
            response["mb"]["memmory_used"] = bytes_to_megabytes(response["b"]["memmory_used"])
            response["mb"]["memmory_free"] = bytes_to_megabytes(response["b"]["memmory_free"])
            response["mb"]["disk_total"] = bytes_to_megabytes(response["b"]["disk_total"])
            response["mb"]["disk_used"] = bytes_to_megabytes(response["b"]["disk_used"])
            response["mb"]["disk_free"] = bytes_to_megabytes(response["b"]["disk_free"])

            response["gb"] = {}
            response["gb"]["memmory_total"] = bytes_to_gigabytes(response["b"]["memmory_total"])
            response["gb"]["memmory_used"] = bytes_to_gigabytes(response["b"]["memmory_used"])
            response["gb"]["memmory_free"] = bytes_to_gigabytes(response["b"]["memmory_free"])
            response["gb"]["disk_total"] = bytes_to_gigabytes(response["b"]["disk_total"])
            response["gb"]["disk_used"] = bytes_to_gigabytes(response["b"]["disk_used"])
            response["gb"]["disk_free"] = bytes_to_gigabytes(response["b"]["disk_free"])

            response["percent_memmory_used"] = psutil.virtual_memory().percent
            response["percent_cpu_used"] = psutil.cpu_percent(interval=1)
            response["cpu_total"] = os.cpu_count()
            response["uptime"] = os.popen('uptime -p').read()[3:-1]

            return response
        
        # content_length = int(self.headers['Content-Length'])
        # request_body = json.loads(
        #     self.rfile.read(content_length).decode('utf-8')
        # )

        metric = metric_collector()
        response_body = json.dumps(metric).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", len(response_body))
        self.end_headers()
        self.wfile.write(response_body)


if __name__ == "__main__":
    httpd = HTTPServer((HOST, PORT), RequestHandler)
    httpd.serve_forever()