#!/usr/bin/env python
import os, socket, ssl
import paho.mqtt.client as paho
from time import time, sleep
from random import uniform
from datetime import datetime

connflag = False

def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

awshost = "a1arqmop0meczp.iot.us-west-2.amazonaws.com"
awsport = 8883
caPath = "./ssl/root-CA.crt"
certPath = "./ssl/cert.pem"
keyPath = "./ssl/private.pem"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
mqttc.connect(awshost, awsport, keepalive=60)
mqttc.loop_start()

while 1==1:
    if connflag == False:
        print("waiting for connection...")
    else:
        temp_reading = uniform(20.0,25.0)
        humidity_reading = uniform(50.0,90.0)
        json_data = """
{
    "serial_number": "39e0cf91_b28a_40c7_aacf_6a88a499816d",
	"timestamp": %f,
	"data": {
		"temperature": %s,
		"humidity": %s
	}
}
""" % (time(), temp_reading, humidity_reading) 
# decode datetime.datetime.utcfromtimestamp(1486185728.525491)
        try:
            mqttc.publish("topic/iot/39e0cf91_b28a_40c7_aacf_6a88a499816d", json_data, qos=1)
            print("msg sent.... \n%s" % json_data )
        except:
            print(traceback.print_exc())
    sleep(60)



