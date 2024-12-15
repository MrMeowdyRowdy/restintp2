from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

# Configuración de Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la tabla reservations
class Reservation(db.Model):
    reservation_id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default="active")

# Inicialización de la base de datos
with app.app_context():
    db.create_all()

# Endpoint para crear una reserva
@app.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.json
    # Verificar disponibilidad con el servicio SOAP
    soap_url = "http://localhost:5000/soap"  # Cambiar si el servicio SOAP está en otro host
    soap_request = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://luxurystay.com/soap">
        <soapenv:Header/>
        <soapenv:Body>
            <soap:getAvailability>
                <soap:start_date>{data['start_date']}</soap:start_date>
                <soap:end_date>{data['end_date']}</soap:end_date>
                <soap:room_type>{data['room_type']}</soap:room_type>
            </soap:getAvailability>
        </soapenv:Body>
    </soapenv:Envelope>
    """
    headers = {'Content-Type': 'text/xml'}
    response = requests.post(soap_url, data=soap_request, headers=headers)

    if "room" not in response.text:
        return jsonify({"error": "No rooms available"}), 400

    # Registrar la reserva en la base de datos
    new_reservation = Reservation(
        room_number=data['room_number'],
        customer_name=data['customer_name'],
        start_date=data['start_date'],
        end_date=data['end_date'],
        status="active"
    )
    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({"message": "Reservation created", "reservation_id": new_reservation.reservation_id}), 201

# Endpoint para consultar una reserva
@app.route('/reservations/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404

    return jsonify({
        "reservation_id": reservation.reservation_id,
        "room_number": reservation.room_number,
        "customer_name": reservation.customer_name,
        "start_date": reservation.start_date,
        "end_date": reservation.end_date,
        "status": reservation.status
    })

# Endpoint para cancelar una reserva
@app.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404

    db.session.delete(reservation)
    db.session.commit()

    return jsonify({"message": "Reservation cancelled"}), 200

# Ejecutar el servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
