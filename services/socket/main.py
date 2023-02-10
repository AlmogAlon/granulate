import json
import logging
import time
from typing import Dict
from bottle import request
from geventwebsocket import WebSocketError
from websocket import WebSocket

from common import engine, utils, abort
from common.async_task import AsyncTask
from granulate.notification import get, Message
from common.settings import project_settings

app = engine.create_app()

sockets: Dict[int, WebSocket] = {}


def handle_notification(data: Dict):
    logging.info(f"handle_notification(): {data}")
    msg = Message.from_dict(data)
    socket = sockets.get(msg.user_id)
    if socket:
        socket.send(json.dumps(msg.to_dict()))
        # todo: send ack
    else:
        logging.info(f"no socket found for user_id: {msg.user_id}")


@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort.soft(code="WEBSOCKET_REQUIRED", reason="Websocket is required")

    user_id = int(request.query.get("user_id"))
    sockets[user_id] = wsock
    while True:
        try:
            message = wsock.receive()
            time.sleep(3)
            wsock.send("Your message was: %r" % message)
        except WebSocketError as e:
            sockets.pop(user_id)
            logging.error("Websocket error: %s", e)
            break


if __name__ == "__main__":
    settings = project_settings().websocket
    port = settings.port
    utils.initialize_logging_to_stdout()

    from gevent.pywsgi import WSGIServer
    from socketserver import ThreadingMixIn
    from geventwebsocket.handler import WebSocketHandler

    class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
        daemon_threads = True

    class Server:
        def __init__(self, wsgi_app, listen="0.0.0.0", app_port=port):
            self.wsgi_app = wsgi_app
            self.listen = listen
            self.port = app_port
            self.server = ThreadingWSGIServer(
                (self.listen, self.port), self.wsgi_app, handler_class=WebSocketHandler
            )

        def serve_forever(self):
            self.server.serve_forever()

    # Listen for notifications
    AsyncTask(get, handle_notification)

    logging.info(f"Serving on port: {port}")
    httpd = Server(app, app_port=port)
    httpd.serve_forever()
