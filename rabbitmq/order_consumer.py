"""Order Event Consumer - processes order events from RabbitMQ."""
import pika
import json
import sys

QUEUE = "order_events"

credentials = pika.PlainCredentials("admin", "admin")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue=QUEUE, durable=True)

total_revenue = 0
processed = 0


def process_order(ch, method, properties, body):
    global total_revenue, processed
    order = json.loads(body.decode())

    subtotal = order["quantity"] * order["price"]
    total_revenue += subtotal
    processed += 1

    print(
        f"[Consumer] Processing order #{order['order_id']}: "
        f"{order['item']} x{order['quantity']} = Rp{subtotal:,}"
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE, on_message_callback=process_order)

print(f"[Consumer] Waiting for order events on queue '{QUEUE}'...")
print("[Consumer] Press CTRL+C to exit.\n")

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

print(f"\n[Consumer] Processed {processed} orders. Total revenue: Rp{total_revenue:,}")
connection.close()
