#!/usr/bin/env python
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt

host='a1arqmop0meczp.iot.us-west-2.amazonaws.com'
rootCAPath="../ssl/root-CA.crt"
certificatePath="../ssl/cert.pem"
privateKeyPath="../ssl/privkey.pem"

logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

client = None
client = AWSIoTMQTTClient("basicPubSub")
client.configureEndpoint(host, 8883)
client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)

client.connect()

loopCount = 0

json_data = """
{ 
    "serial_number":7654321,
    "temperature": 123,
    "humidity": 456
}"""
client.publish("topic/iot1/data", json_data, 1)
loopCount += 1


