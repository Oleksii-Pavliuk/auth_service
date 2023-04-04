# Authentication service for transactions app


## Transactions50 is my final project for Harvards CS50 Web Programing with Python and JavaScript
This app allow users to buy,sell,withdraw,send cryptocurency, to process fiat operations app using PayPal API, to do cryprocurency operations app using MetaMask API.

To do this user needs to have account in application, there is two tipes of accounts; Basic and Full. 

 - Basic - standart account with no KYC, just email and password. Allows users to deposit, withdraw and send cryptocurency within ETH network.
 - Full - account with KYC verification allows users to deposit fiat,withdraw fiat, buy cryptocurency and sell it.

It consists of 5 microservices:
 - Authentication service 
 - User managment service
 - Payment gateway service
 - Transactions service
 - Walet integration service

And front-end React app
<img width="895" alt="Screenshot 2023-04-04 at 11 16 03 am" src="https://user-images.githubusercontent.com/71220725/229661212-803393b4-1627-44c0-8137-e251817aae1c.png">

## Services description:

### Authentication service 
Django REST API connected to PostgreSQL database with users credentials used to create new user, authenticate user, change user's password or email, delete user's account. As a method of comunication app using http, so its standart REST API.

To secure API http request must include eather API KEY or Authorisation credentials to make successful request.

App running in container and connected to Consul server and postgreSQL server.

To run this container running consul containers (```infrastructure/platform/docker-compose.yml```) and postgres container (```infrastructure/users-postgresDB-deploy.sh```) <b>at least!!!</b> required.

All settings of Django app contains in docker run script named ```infrastructure/auth-service-deploy.sh``` and may be specified in it before running, all sensitive data should be stored in Kubernetes or Docker swarm secrets. 
#### To obtain API key:
After starting container, go to containers shell 
        

            docker exec -it <container_id> bash

in there apply migrations

  
            python3 manage.py migrate
   
than go to python shell

 
            python3 manage.py shell
  
in there execute:

    from rest_framework_api_key.models import APIKey

    api_key, key = APIKey.objects.create_key(name="<service_name>")

and print key: 

```print(key)```

### User managment service
Express server built with Typescript using PostgreSQL to store transactions data and MongoDB to store users data.
This server will act as gateway from frontend app and will recive all requests from client and then send data to other services via HTTP or RabitMQ.
    
All routes will be secured with JWT authentication with 2h expiration time, to obtain JWT user needs to pass authorisation (login in front-end app).

To run this container running consul containers (```infrastructure/platform/docker-compose.yml```), postgres container (```infrastructure/transactions-postgresDB-deploy.sh```) and mongoDB container (```infrastructure/users-mongoDB-deploy.sh```) <b>at least!!!</b> required.

All settings of Express app contains in docker run script named ```infrastructure/userManagment-service-deploy.sh``` and may be specified in it before running, all sensitive data should be stored in Kubernetes or Docker swarm secrets. 

To do requests to authentication service we need to specify API_KEY in container deployment script (```infrastructure/userManagment-service-deploy.sh```)




