import pika
import json
from api.db import db_session
from api.db.models import Booking, BookingStatus
from time import sleep
import random

def callback(ch, method, properties, body):
    message = json.loads(body)
    booking_id = message["booking_id"]
    timeslot = message["timeslot"]
    patient_email = message["patient_email"]
    
    # Simulación del proceso de confirmación (retraso artificial)
    sleep(random.randint(2, 5))  # Simula el retraso entre 2 y 5 segundos
    
    # Simulamos la disponibilidad médica
    is_available = random.choice([True, False])
    
    # Obtener la reserva desde la base de datos
    booking = db_session.query(Booking).filter(Booking.id == booking_id).first()
    
    if booking:
        if is_available:
            booking.status = BookingStatus.CONFIRMED
        else:
            booking.status = BookingStatus.REJECTED
        db_session.commit()

        # Enviar una notificación de confirmación o rechazo
        notification = {
            "email": patient_email,
            "status": booking.status.value,
            "timeslot": timeslot
        }
        send_notification(notification)
    
    # Confirmar que el mensaje fue procesado
    ch.basic_ack(delivery_tag=method.delivery_tag)

def send_notification(notification):
    # Aquí simularíamos el envío de un correo electrónico (puedes integrarlo con un servicio real más tarde)
    print(f"Enviando notificación al email {notification['email']} - Estado: {notification['status']}")

def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    # Declarar la cola
    channel.queue_declare(queue="solicitar_cita", durable=True)

    # Consumir mensajes de la cola
    channel.basic_consume(queue="solicitar_cita", on_message_callback=callback)
    print("Esperando mensajes de RabbitMQ. Para salir, presiona CTRL+C.")
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()
