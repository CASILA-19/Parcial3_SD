from api.db.models import Booking, BookingStatus
from api.db import db_session
from api.utils.rabbitmq import send_to_queue
from datetime import datetime

def create_booking(data):
    # Crear una nueva reserva
    new_booking = Booking(
        patient_name=data["patient_name"],
        patient_email=data["patient_email"],
        timeslot=data["timeslot"]
    )
    
    # Guardar en la base de datos
    db_session.add(new_booking)
    db_session.commit()
    
    # Enviar la solicitud de cita a RabbitMQ (cola 'solicitar_cita')
    send_to_queue('solicitar_cita', {
        "booking_id": new_booking.id,
        "timeslot": new_booking.timeslot,
        "patient_email": new_booking.patient_email
    })
    
    return new_booking

def get_booking(booking_id):
    # Obtener una reserva por su ID
    return db_session.query(Booking).filter(Booking.id == booking_id).first()
