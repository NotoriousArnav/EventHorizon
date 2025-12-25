import threading
import requests
import json
import logging
from django.core.serializers.json import DjangoJSONEncoder

logger = logging.getLogger(__name__)


def trigger_webhook_async(url, payload):
    """
    Sends a webhook request in a separate thread.
    """

    def send_request():
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                url,
                data=json.dumps(payload, cls=DjangoJSONEncoder),
                headers=headers,
                timeout=5,
            )
            response.raise_for_status()
            logger.info(
                f"Webhook sent successfully to {url}. Status: {response.status_code}"
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send webhook to {url}: {str(e)}")

    thread = threading.Thread(target=send_request)
    thread.daemon = True
    thread.start()
