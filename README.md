Para ejecutar el proyecto realiza lo siguiente en una consola con docker dentro de la carpeta del mismo.

docker build -t rest-service .

docker run -d -p 5001:5001 --name rest-container rest-service

Podrás acceder a el a traves de 

http://localhost:5001/reservations