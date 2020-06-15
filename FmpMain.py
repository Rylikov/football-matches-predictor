import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from FmpPredictor import FmpPredictor


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header("Content-type", "application/json")
        self.end_headers()

        Predictor2 = FmpPredictor('Everton', 'Southampton')

        message = json.dumps(Predictor2.get_predictions())
        print(message)
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


def run():
    print('starting server...')
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()



