from sites import *
import time
import pika
import json

MIN = 10
toBeChecked = [EconomicTimes, DainikBhaskar]

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()
channel.queue_declare(queue = 'toCrawl')

def sendRequest(jsonObject):
    print("Sending...")
    channel.basic_publish(exchange = '', routing_key = 'toCrawl', body = json.dumps(jsonObject))


if __name__ == '__main__':
    while True:
        for site in toBeChecked:
            sendRequest(site().run())
        time.sleep(MIN * 60)