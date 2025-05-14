import pika
import json

def send_notification(notification):
    # Aquí se puede simular o integrar con un servicio real de correos
    print(f"Enviando correo a {notification['email']}:")
    print(f"Estado de la cita: {notification['status']}")
    print(f"Franja horaria: {notification['timeslot']}")
    print("Correo enviado correctamente!")

def callback(ch, method, properties, body):
    message = json.loads(body)
    send_notification(message)

    # Confirmar que el mensaje fue procesado
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    # Declarar la cola de notificaciones
    channel.queue_declare(queue="booking_notifications", durable=True)

    # Consumir mensajes de la cola
    channel.basic_consume(queue="booking_notifications", on_message_callback=callback)
    print("Esperando mensajes de RabbitMQ para enviar notificaciones.")
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()
