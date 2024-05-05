# FastAPI-ProductAPI
FastAPI project demonstrating a CRUD API for managing products. Includes endpoints for creating, reading, updating, and deleting products, with authentication and authorization using JWT tokens."

# Product API

This project is a FastAPI application that provides endpoints to manage products. It includes authentication using JWT tokens.

## Features

- Create, read, update, and delete products
- User authentication and authorization using JWT tokens
- Secure password storage using bcrypt

## Requirements

- Python 3.7+
- MySQL database
- Required Python packages (install using `pip install -r requirements.txt`)

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   
2.install dependencies:

  pip install -r requirements.txt

3. Set up the database:
  Create a MySQL database
  Update the database URL in database.py

4.Run the application:
  uvicorn main:app --reload

5.Access the API at http://localhost:8000/docs and authenticate using the provided endpoints.
API Endpoints:
  1.POST /auth/token: Get a JWT token for authentication
  2.POST /products/: Create a new product
  3.GET /products/: Retrieve all products
  4.GET /products/{product_id}: Retrieve a specific product
  5.PUT /products/{product_id}: Update a product
  6.DELETE /products/{product_id}: Delete a product

6.Authentication
To authenticate, use the /auth/token endpoint with a valid username and password. Include the token in the Authorization header for other endpoints.

7.Author
Chandni Thakkar
