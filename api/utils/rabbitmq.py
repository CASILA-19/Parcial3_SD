import pika
import json
import os

# Función para enviar un mensaje a la cola de RabbitMQ
def send_to_queue(queue_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST', 'localhost')))
    channel = connection.channel()

    # Declarar la cola
    channel.queue_declare(queue=queue_name, durable=True)

    # Publicar el mensaje
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Mensaje persistente
        )
    )
    
    connection.close()
