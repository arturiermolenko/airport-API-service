# Airport service API system
This is API for Airport management system. Based on it, You can create a website with possibilities of viewing flights, routes, airports with its city and country, airplanes with its owner airline company and type of airplane, making your own order with tickets. You can also find out the quantity of available tickets for the flight.


# The applicatios has following database structure:
![ScreenShot](/schema.jpg)


## Installing / Getting started

A quick introduction of the minimal setup you need to get a Airport app up &
running. With this You will run server with cleane Database.

### Python3 must be already installed!

### You also need to install PostgreSQL and create a database.

```shell
git clone https://github.com/arturiermolenko/airport-API-service
cd airport_API_service
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
touch .env
python manage.py migrate
python manage.py runserver
```
Instead of "touch .env" use, please, command "echo > .env" for Windows.
Fill .env file in according to .env_sample

## Running with Docker

Docker must be already installed!

Uncomment string MEDIA_ROOT = "/vol/web/media" in setting.py

```shell
git clone https://github.com/arturiermolenko/airport-API-service
docker-compose biuld
docker-compose up
```

Use the following command to load prepared data from fixture:
```shell
python manage.py loaddata airport_data.json
```


## Features:
- JWT authenticated:
- Admin panel: /admin/
- Documentation is located at: </api/doc/swagger/>, </api/doc/redoc/>
- Create planes with owner airplines and airplane types
- Creatte airports with in different cities and countries
- Create routes from one airport to another
- Create flights with route, airplane
- Make Your orders with tickets

## Getting access
You can create superuser with :
```shell
python manage.py createsuperuser
```
or create a default user using api/user/register/

To work with token use:

- get access token and refresh token http://127.0.0.1:8000/api/user/token/
- refresh access token http://127.0.0.1:8000/api/user/token/refresh/
- verify access token http://127.0.0.1:8000/api/user/token/verify/

Note: Make sure to send Token in api urls in Headers as follows:

- key: Authorization

- value: Bearer @token

Airport API allows:
- using api/admin/ --- Work with admin panel
- using /api/doc/swagger/ --- Detail api documentation by swagger
- using /api/doc/redoc/ --- Detail api documentation by redoc
- using [GET] /api/user/me/ --- Information about user
- using [PUT, PATCH] /api/user/me/ --- Update user information
- using [POST] /api/user/register/ --- Register a new user
- using [POST] /api/user/token/ --- Obtain new Access and Refresh tokens using credential
- using [POST] /api/user/token/refresh/ --- Obtain new Access token using refresh token
- using [POST] /api/user/token/verify/ --- Verify Access token
######
- using [GET] /api/airplane/airplane-types/ --- Airplane types list
- using [POST] /api/airplane/airplane-types/ --- Add new type off airplane
- using [GET] /api/airplane/airlines/ --- Airlines list
- using [POST] /api/airplane/airlines/ --- Add new airline
- using [GET] /api/airplane/airplanes/ --- Airplanes list
- using [POST] /api/airplane/airplanes/ --- Add new airplane
######
- using [GET] /api/airport/airports/ --- Airports list
- using [POST] /api/airport/airports/ --- Add new airport
- using [GET] /api/airport/cities/ --- Cities list
- using [POST] /api/airport/cities/ --- Add new city
- using [GET] /api/airport/countries/ --- Countries list
- using [POST] /api/airport/countries/ --- Add new country
- using [GET] /api/airport/routes/ --- Routes list
- using [POST] /api/airport/routes/ --- Add new route
- using [GET] /api/airport/routes/{id}/ --- Detail info aboute route
######
- using [GET] /api/flight/crew-members/ --- Crew members list
- using [POST] /api/flight/crew-members/ --- Add new crew member
- using [GET] /api/flight/flights/ --- Flights list
- using [POST] /api/flight/flights/ --- Add new flight
- using [GET] /api/flight/flights/{id}/ --- Detail info about flight
- using [PUT] /api/flight/flights/{id}/ --- Change all ingo about flight
- using [PATCH] /api/flight/flights/{id}/ --- Partial info change about flight
- using [DELETE] /api/flight/flights/{id}/ --- Delete flight
- using [GET] /api/flight/orders/ --- Orders list of current user
- using [POST] /api/flight/orders/ --- Create new order
- using [GET] /api/flight/orders/{id}/ --- Detail info about order of current user
