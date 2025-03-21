import os
import json
import threading
from urllib.parse import urlparse

import paho.mqtt.client as mqtt

# Import your db session from step 1
from db.session import db

class MQTTManager:
    def __init__(self, broker_url: str = None, topic: str = "test/topic"):
        # Use broker_url from argument or environment, or fallback to default
        self.broker_url = broker_url or os.getenv("MQTT_BROKER_URL", "mqtt://mqtt:1883")
        self.topic = topic
        self.lock = threading.Lock()
        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        """
        Handle incoming MQTT messages. In this example:
        1. Decode the payload from bytes to string.
        2. Attempt to parse the message as JSON.
        3. Insert into MongoDB.
        """
        message_str = msg.payload.decode('utf-8')
        print(f"Received message on topic '{msg.topic}': {message_str}")

        # Attempt to parse the incoming data as JSON
        try:
            data = json.loads(message_str)
        except json.JSONDecodeError:
            # If it isn't valid JSON, just store the raw message
            data = {"raw_message": message_str}

        # Prepare a document to insert into MongoDB
        document = {
            "topic": msg.topic,
            "data": data
        }

        # Insert into a collection named "logs" (change as needed)
        db["logs"].insert_one(document)

    def start(self):
        """
        Connect to the MQTT broker and start the background loop.
        """
        parsed_url = urlparse(self.broker_url)
        host = parsed_url.hostname or "mqtt"
        port = parsed_url.port or 1883
        self.client.connect(host, port, 60)
        self.client.loop_start()  # Start background thread for MQTT processing
