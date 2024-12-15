Para ejecutar el proyecto realiza lo siguiente en una consola con docker dentro de la carpeta del mismo.

docker build -t rest-service .

docker run -d -p 5001:5001 --name rest-container rest-service

Podrás acceder a el a traves de 

http://localhost:5001/reservations

Pruebas
Crear Reserva: Endpoint: POST http://localhost:5001/reservations

{
  "room_number": 3,
  "customer_name": "Alice Brown",
  "start_date": "2024-12-16",
  "end_date": "2024-12-16",
  "room_type": "Suite"
}

Consultar Reserva: Endpoint: GET http://localhost:5001/reservations/{id}

Cancelar Reserva: Endpoint: DELETE http://localhost:5001/reservations/{id}