import logging

from utils import utils
from router import engine
from routes.chat import app as chat_app

app = engine.create_app()

app.mount("/chat", chat_app)

if __name__ == "__main__":
    PORT = 1337
    utils.initialize_logging_to_stdout()

    from wsgiref.simple_server import make_server, WSGIServer
    from socketserver import ThreadingMixIn

    class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
        daemon_threads = True

    class Server:
        def __init__(self, wsgi_app, listen="0.0.0.0", port=8080):
            self.wsgi_app = wsgi_app
            self.listen = listen
            self.port = port
            self.server = make_server(self.listen, self.port, self.wsgi_app, ThreadingWSGIServer)

        def serve_forever(self):
            self.server.serve_forever()

    logging.info(f"Serving on port: {PORT}")
    httpd = Server(app, port=PORT)
    httpd.serve_forever()
