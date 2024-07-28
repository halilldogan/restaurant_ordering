# Restaurant Ordering Application

This project is a REST API service that accepts user orders, processes these orders through a Redis Pub/Sub system, and finally lists the orders. The project is built using Django, Redis, and runs within Docker containers.

## Requirements

- Docker
- Docker Compose

## Installation and Setup

### Clone the Repository

```sh
git clone https://github.com/halilldogan/restaurant_ordering.git
cd restaurant_ordering
```
### Create Docker Compose File
Create docker-compose.yml in the project directory with the following content:
```yaml
version: '3'

services:
  db:
    image: mysql:8.0-debian
    restart: always
    container_name: mysql
    environment:
      ENGINE: 'django.db.backends.mysql'
      MYSQL_ROOT_PASSWORD: your_password
      TZ: Europe/Istanbul
    ports:
      - 3306:3306
    volumes:
      - db-volume:/var/lib/mysql
  
  redis:
    image: redis:latest
    ports: 
      - 6379:6379
      
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    image: django-app
    restart: always
    container_name: django-app
    volumes:
      - .:/app
    ports:
      - 8000:8000
    environment:
        DATABASE_NAME: restaurantdb
        DATABASE_USER: root
        DATABASE_PASSWORD: your_password
        DATABASE_HOST: db
        DATABASE_PORT: 3306
        REDIS_HOST: redis
    depends_on:
      - db
      - redis
    
  subscriber:
    build: .
    command: python subscriber.py
    depends_on:
      - redis
      - web
    environment:
        - REDIS_HOST=redis
        - APP_BASEURL=http://web:8000
    
volumes:
  web-volume: 
  db-volume:
```

### Start the Django Project
Start the Docker containers and apply the necessary migrations:

```sh
docker-compose up --build
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

## Using the API
You can now use the API. By default, it will be running at http://localhost:8000/api.

### Running Tests
To run tests, use the following command:

```sh
docker-compose run web python manage.py test orders
```

### API Endpoints

Create Order: POST api/orders/submit_order/

Finalize Order: This endpoint listens to the Redis channel and runs when the order is submitted.

List Orders: GET api/orders/list_orders/

### Contributors

halilldogan
