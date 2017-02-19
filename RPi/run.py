import paho.mqtt.client as mqtt
import re
import json
import time

HOST_NAME = "www.kbumsik.net"
LOCATION_NAME = "HackCEWIT"
USER_NAME = "defaultUser"
USER_PASSWORD = "dummypassword"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Start collecting data...")
    client.subscribe("control/#")
    #client.subscribe("control/" + USER_NAME + "/" + LOCATION_NAME + "/+")
    client.on_message = on_message
    pass

topic_regex = re.compile("control\/" + USER_NAME + "\/" + LOCATION_NAME + "\/(\w+)")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload.decode("utf-8"))["content"]
    print(topic + " is updated: " + str(payload))

    matched = topic_regex.match(topic)
    if matched:
        device_name = matched.group(1)
        # update payload
        print(device_name + " is updated: " + str(payload))
        if device_name == "Relay":
            input = payload["switch"]
            if input == "On":
                GPIO.output(20, GPIO.LOW)
            else:
                GPIO.output(20, GPIO.HIGH)
        else:
            pass

    pass

if __name__ == "__main__":
    # MQTT connecting
    client = mqtt.Client()
    # This will msg will discard its topic
    #client.will_set(topic="status/server/" + id, payload='', qos=0, retain=True)
    client.on_connect = on_connect

    try:
        client.connect(host=HOST_NAME, port=1883, keepalive=60)
    except:
        print('Failed to connect to the server')
        exit()
    else:
        print('Connection Success!')
        #payload = '{"content":{"switch":true,"Green":93,"temp":50.98,"msg":"RPi"},"password":"dummypassword"}'
        #client.publish(topic="record/defaultUser/defaultRoom1/defaultDevice2", payload=payload, qos=1)

    # Start mqtt Comm.client
    print('RPi is ready for any event...')
    client.loop_start()

    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    # PB
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    pb_state = GPIO.input(21)
    # Relay
    GPIO.setup(20, GPIO.OUT)
    GPIO.output(20, GPIO.HIGH)

    topic_root = "record/" + USER_NAME + "/" + LOCATION_NAME + "/"
    # Polling sensor change
    while True:
        # update change
        # Push button
        pb_state_now = GPIO.input(21)
        if pb_state_now != pb_state:
            print("Button Changed!")
            if not pb_state_now:
                payload = '{"content":{"switch":"On"},"password":"dummypassword"}'
            else:
                payload = '{"content":{"switch":"Off"},"password":"dummypassword"}'
            client.publish(topic= topic_root + "RPi_1", payload=payload, qos=1)
        pb_state = pb_state_now
        # Others

        time.sleep(0.5)
