# Database Design

## Overview

This document defines the database structure for the marketplace.

The application will use PostgreSQL as its primary relational database.

The schema is designed to be normalized, scalable, and easy to maintain.

This document describes the tables and their relationships. Detailed columns and constraints will be added during implementation.

---

# Design Principles

- PostgreSQL is the source of truth.
- Each table represents one business entity.
- Avoid duplicate data.
- Use foreign keys to define relationships.
- Design for scalability.
- Keep business logic outside the database whenever possible.

---

# Database Modules

## User Module

Tables

- users
- user_profiles
- user_addresses
- user_sessions

---

## Authentication Module

Tables

- email_verifications
- password_resets

---

## Seller Module

Tables

- sellers
- seller_verifications
- seller_payouts

---

## Product Catalog Module

Tables

- brands
- categories
- products
- product_variants
- product_images
- product_specifications

---

## Inventory Module

Tables

- inventory

---

## Marketplace Module

Tables

- wishlists
- wishlist_items

- carts
- cart_items

---

## Order Module

Tables

- orders
- order_items

---

## Payment Module

Tables

- payments
- refunds

---

## Shipping Module

Tables

- shipments
- shipment_tracking

---

## Review Module

Tables

- product_reviews
- seller_reviews

---

## Trust & Safety Module

Tables

- disputes
- fraud_reports

---

## Notification Module

Tables

- notifications

---

## Administration Module

Tables

- audit_logs

---

# High-Level Relationships

User
├── Profile
├── Address
├── Wishlist
├── Cart
├── Orders
└── Reviews

Seller
└── Inventory

Inventory
└── Product Variant

Product Variant
└── Product

Product
├── Brand
└── Category

Order
├── Order Items
├── Payment
└── Shipment

Shipment
└── Tracking

Order
└── Dispute

Product
└── Product Reviews

Seller
└── Seller Reviews

---

# Future Tables

These tables are planned but are not part of the initial MVP.

- price_history
- auctions
- bids
- community_posts
- comments
- reactions
- follows
- recommendations
- ai_predictions
- event_feeds
- event_media

---

# Notes

This document intentionally focuses only on the overall database structure.

The following implementation details will be defined during development:

- Columns
- Data Types
- Primary Keys
- Foreign Keys
- Constraints
- Indexes
- Cascading Rules