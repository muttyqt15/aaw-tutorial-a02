import pika
import sys

MAX_MSGS = int(sys.argv[1]) if len(sys.argv) > 1 else 3

credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue='hello')

count = [0]

def callback(ch, method, properties, body):
    msg = f"[x] Received {body.decode()}"
    print(msg, flush=True)
    count[0] += 1
    if count[0] >= MAX_MSGS:
        ch.stop_consuming()

channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
print(f'[*] Waiting for up to {MAX_MSGS} messages...', flush=True)
channel.start_consuming()
connection.close()
