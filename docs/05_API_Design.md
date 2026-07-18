# API Design

## Overview

This document defines the REST API for the marketplace.

The backend will be built using FastAPI.

The API will follow REST principles and communicate using JSON.

Authentication will use JWT tokens.

This document will evolve as new features are added.

---

# API Design Principles

- RESTful endpoints
- JSON request and response bodies
- Stateless authentication using JWT
- Consistent error responses
- Resource-based URLs
- API versioning

Example:

/api/v1/

---

# Authentication

POST    /auth/register

POST    /auth/login

POST    /auth/logout

POST    /auth/refresh-token

POST    /auth/forgot-password

POST    /auth/reset-password

GET     /auth/me

---

# Users

GET     /users/me

PATCH   /users/me

DELETE  /users/me

GET     /users/me/addresses

POST    /users/me/addresses

PATCH   /users/me/addresses/{id}

DELETE  /users/me/addresses/{id}

---

# Sellers

GET     /sellers

GET     /sellers/{seller_id}

POST    /sellers/apply

PATCH   /sellers/profile

GET     /sellers/dashboard

GET     /sellers/inventory

---

# Brands

GET     /brands

GET     /brands/{brand_id}

---

# Categories

GET     /categories

GET     /categories/{category_id}

---

# Products

GET     /products

GET     /products/{product_id}

GET     /products/search

POST    /products

PATCH   /products/{product_id}

DELETE  /products/{product_id}

---

# Product Variants

GET     /variants/{variant_id}

POST    /variants

PATCH   /variants/{variant_id}

DELETE  /variants/{variant_id}

---

# Inventory

GET     /inventory

POST    /inventory

PATCH   /inventory/{inventory_id}

DELETE  /inventory/{inventory_id}

---

# Wishlist

GET     /wishlist

POST    /wishlist

DELETE  /wishlist/{item_id}

---

# Cart

GET     /cart

POST    /cart/items

PATCH   /cart/items/{item_id}

DELETE  /cart/items/{item_id}

---

# Orders

GET     /orders

GET     /orders/{order_id}

POST    /orders

PATCH   /orders/{order_id}

POST    /orders/{order_id}/cancel

---

# Payments

POST    /payments

GET     /payments/{payment_id}

GET     /payments/history

POST    /refunds

---

# Shipping

GET     /shipments

GET     /shipments/{shipment_id}

GET     /shipments/{shipment_id}/tracking

---

# Reviews

GET     /products/{product_id}/reviews

POST    /products/{product_id}/reviews

PATCH   /reviews/{review_id}

DELETE  /reviews/{review_id}

GET     /sellers/{seller_id}/reviews

---

# Disputes

POST    /disputes

GET     /disputes/{dispute_id}

PATCH   /disputes/{dispute_id}

---

# Notifications

GET     /notifications

PATCH   /notifications/{notification_id}/read

---

# Admin

GET     /admin/users

GET     /admin/sellers

GET     /admin/orders

GET     /admin/disputes

PATCH   /admin/users/{user_id}

PATCH   /admin/orders/{order_id}

PATCH   /admin/disputes/{dispute_id}

---

# Future APIs

- Price History
- AI Recommendations
- Price Prediction
- Community Feed
- Events
- Auctions
- Bidding
- Messaging
- Follow System

---

# Notes

This document defines the public API surface of the application.

The following implementation details will be defined during development:

- Request Body
- Response Body
- Status Codes
- Validation Rules
- Authentication Requirements
- Rate Limiting
- Permissions