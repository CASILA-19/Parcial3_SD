from flask import Blueprint, request, jsonify
from api.services.booking_service import create_booking, get_booking

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/book", methods=["POST"])
def book_appointment():
    data = request.get_json()
    if not all(k in data for k in ("patient_name", "patient_email", "timeslot")):
        return jsonify({"error": "Missing required fields"}), 400
    booking = create_booking(data)
    return jsonify({"booking_id": booking.id}), 201

@booking_bp.route("/booking/<int:booking_id>", methods=["GET"])
def get_booking_status(booking_id):
    booking = get_booking(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify({
        "id": booking.id,
        "status": booking.status.value,
        "patient": booking.patient_name,
        "email": booking.patient_email,
        "timeslot": booking.timeslot,
        "created_at": booking.created_at.isoformat()
    })
