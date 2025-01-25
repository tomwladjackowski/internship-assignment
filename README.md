# Wolt Internship Backend Project

This is a project made as a part of appliaction for the Backend Engineer Internship 2025 Programme at Wolt
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


## Installation

Step-by-step instructions on how to install and set up the project locally.

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

### Running with Docker:

Build and run the Docker container:
```bash
# Build the Docker image
docker build -t project-name .

# Run the Docker container
docker run -p 8000:8000 project-name
```
The project server should be running at localhost:8000.

---

## Usage

How to use the project. Include example commands or API endpoint usage if applicable.

### Running the Application:
```bash
$ uvicorn main:app --reload
```

### Example API Call:
```bash
GET /api/v1/delivery-order-price
```
Query Parameters:
- `cart_value`: Total value of the cart.
- `venue_slug`: Unique identifier of the venue.
- `user_lat`: User's latitude.
- `user_lon`: User's longitude.

---

## Testing

Provide instructions on how to run the test suite for the project.

### Running Tests:
```bash
$ pytest
```

Ensure you have all necessary test dependencies installed by checking the `requirements-dev.txt` file.

---

## Technologies Used

- **Python**: Core programming language.
- **FastAPI**: Web framework for building APIs.
- **Pytest**: For unit testing.
- **Pydantic**: Data validation and parsing.
- **Requests**: HTTP requests for interacting with external APIs.

