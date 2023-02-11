from datetime import datetime

import requests

from common.settings import project_settings


def send_notification(message_id: int):
    server = project_settings().notification
    requests.post(
        f"http://{server.addr}:{server.port}/api/notification/sent",
        json={
            "message_id": message_id,
            "sent_time": str(datetime.now().isoformat()),
        },
    )
