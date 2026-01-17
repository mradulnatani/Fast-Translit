import pika
import os

def send_notification(message: str, queue: str = "notifications"):
  #  params = pika.URLParameters(RABBIT_URL)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange="", routing_key=queue, body=message)
    connection.close()
