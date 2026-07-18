# Domain Model

This document defines the core business entities that exist within the marketplace and how they relate to one another.

It is independent of the database design and will evolve as the product grows.

---

# Core Principles

- Every real-world concept should have a corresponding domain entity.
- Domain entities describe the business, not the implementation.
- Relationships may change as the product evolves.

---

# Core Entities

## Users

- User
- Buyer
- Seller
- Administrator
- Support Staff

---

## Identity

- User Profile
- Address
- Verification
- Authentication
- Roles
- Permissions

---

## Product Catalog

- Category
- Subcategory
- Brand
- Master Product
- Product Variant
- Product Images
- Product Specifications
- Product Condition

---

## Inventory

- Seller Inventory
- Inventory Item
- Quantity
- Availability
- Asking Price

---

## Marketplace

- Offer
- Wishlist
- Shopping Cart
- Cart Item

---

## Orders

- Order
- Order Item
- Invoice
- Payment
- Refund
- Cancellation

---

## Logistics

- Shipment
- Shipping Method
- Tracking
- Delivery

---

## Trust & Safety

- Review
- Rating
- Authentication Request
- Dispute
- Fraud Report

---

## Communication

- Notification
- Conversation
- Message

---

## Administration

- Dashboard
- Reports
- Audit Log
- Announcement

---

# High-Level Relationships

User
├── Buyer
├── Seller
└── Administrator

Seller
├── owns
└── Inventory

Inventory
├── contains
└── Inventory Item

Inventory Item
├── references
└── Product Variant

Product Variant
├── belongs to
└── Master Product

Master Product
├── belongs to
├── Brand
└── Category

Buyer
├── creates
└── Cart

Buyer
├── places
└── Order

Order
├── contains
└── Order Items

Order
├── has
├── Payment
└── Shipment

Buyer
├── writes
└── Review

Seller
├── receives
└── Review

Order
├── may create
└── Dispute

Administrator
├── manages
├── Users
├── Products
├── Orders
├── Sellers
└── Disputes

---

# Notes

This document intentionally avoids database tables, SQL, APIs, and implementation details.

Its purpose is to define the language of the business.

Every future database table, API endpoint, backend model, and frontend screen should map back to one or more of these domain entities.