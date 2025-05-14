import pika
import json
from api.db import db_session
from api.db.models import Booking, BookingStatus
from api.utils.rabbitmq import send_to_queue

def callback(ch, method, properties, body):
    message = json.loads(body)
    booking_id = message["booking_id"]
    
    # Obtener la reserva desde la base de datos
    booking = db_session.query(Booking).filter(Booking.id == booking_id).first()

    if booking and booking.status == BookingStatus.CONFIRMED:
        # Enviar una notificación de confirmación
        print(f"Cita confirmada para el paciente {booking.patient_name}.")
        send_to_queue('booking_notifications', {
            "email": booking.patient_email,
            "status": "confirmed",
            "timeslot": booking.timeslot
        })
    
    # Confirmar que el mensaje fue procesado
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    # Declarar la cola
    channel.queue_declare(queue="cita_confirmada", durable=True)

    # Consumir mensajes de la cola
    channel.basic_consume(queue="cita_confirmada", on_message_callback=callback)
    print("Esperando mensajes de RabbitMQ para confirmar citas.")
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()
