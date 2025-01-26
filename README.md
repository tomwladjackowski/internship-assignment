# Wolt Internship Backend Project

This is a project made as a part of an appliaction for the Backend Engineer Internship 2025 Programme at Wolt.
---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Testing](#testing)
5. [Technologies Used](#technologies-used)

---


## Overview

This Python project is a service that calculates the total price and price breakdown of a delivery order.
It integrates with Home Assignment API to get data about the venue and calculates the price based on the date included in the query. It is made using FastAPI framework for Python.

---

## Installing the application

### Requirements
 - **Python** >= 3.10 and **pip**
 - **Docker** if you'd like to run with **Docker**

```bash
# Clone the repository
$ git clone https://github.com/your-repo/project-name.git

# Navigate to the project directory
$ cd project-name

# Create and activate a virtual environment
$ python3 -m venv venv
$ source venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt
```

---

## Usage

The API has two endpoints:
- 1.'GET' '/health' - responds to a GET requests with status 200 to show the server is running
- 2.'GET' '/api/v1/deliver-order-price-service' - endpoint for our delivery price calculation service

delivery-order-price-service requires following query parameters:
- 1.venue_slug (string): The unique identifier (slug) for the venue from which the delivery order will be placed
- 2.cart_value: (integer): The total value of the items in the shopping cart
- 3.user_lat (number with decimal point): The latitude of the user's location
- 4.user_lon (number with decimal point): The longitude of the user's location

and returns a response in the following format:
```json
    {
        "total_price": 1190,
        "small_order_surcharge": 0,
        "cart_value": 1000,
        "delivery": {
            "fee": 190,
            "distance": 177
        }
    }
```
where
* `total_price` (integer): The calculated total price
* `small_order_surcharge` (integer): The calculated small order surcharge
* `cart_value` (integer): The cart value. This is the same as what was got as query parameter.
* `delivery` (object): An object containing:
  * `fee` (integer): The calculated delivery fee
  * `distance` (integer): The calculated delivery distance in meters
    
### Running the Application:
```bash
$ uvicorn main:app --reload
```

### Example API Call:
```bash
GET /api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087

```

### Running with Docker:

Build and run the Docker container:
```bash
# Build the Docker image
docker build -t project-name .

# Run the Docker container
docker run -p 8000:8000 project-name
```
The project server should now be running at localhost:8000.

---

## Testing

### Running Tests:
```bash
$ pytest
```

Ensure you have all necessary test dependencies installed by checking the `requirements.txt` file.

---

## Technologies Used

- **Python**: Core programming language.
- **FastAPI**: Web framework for building APIs.
- **Pytest**: For unit testing.
- **Pydantic**: Data validation and parsing.
- **Requests**: HTTP requests for interacting with external APIs.

