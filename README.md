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

