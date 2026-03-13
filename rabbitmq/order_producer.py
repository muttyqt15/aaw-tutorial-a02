"""Order Event Producer - sends order events to RabbitMQ."""
import pika
import json
import time
import sys

QUEUE = "order_events"

credentials = pika.PlainCredentials("admin", "admin")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue=QUEUE, durable=True)

orders = [
    {"order_id": 1, "item": "Laptop", "quantity": 1, "price": 15000000},
    {"order_id": 2, "item": "Mouse", "quantity": 2, "price": 250000},
    {"order_id": 3, "item": "Keyboard", "quantity": 1, "price": 750000},
    {"order_id": 4, "item": "Monitor", "quantity": 1, "price": 4500000},
    {"order_id": 5, "item": "Headset", "quantity": 3, "price": 500000},
]

print(f"[Producer] Sending {len(orders)} order events to queue '{QUEUE}'...\n")

for order in orders:
    body = json.dumps(order)
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE,
        body=body,
        properties=pika.BasicProperties(delivery_mode=2),  # persistent
    )
    print(f"[Producer] Sent order #{order['order_id']}: {order['item']} x{order['quantity']} @ Rp{order['price']:,}")
    time.sleep(0.5)

print(f"\n[Producer] All {len(orders)} order events sent successfully.")
connection.close()
