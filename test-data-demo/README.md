# Test Data Generation Demo

This demo showcases using GitHub Copilot to generate test data for an existing test suite.

## Overview

This is a simple **Order Processing System** that validates and processes customer orders. The tests are already written but are missing the test data fixtures needed to run them.

## The Challenge

The test files in `tests/` reference data fixtures that don't exist yet:
- `tests/fixtures/sample_customers.json` - Customer records for testing
- `tests/fixtures/sample_orders.json` - Order records for testing
- `tests/fixtures/sample_products.json` - Product catalog for testing

## Demo Goals

Use Copilot to:
1. Generate realistic test data that matches the expected schemas
2. Create edge case data for boundary testing
3. Generate data that covers various validation scenarios

## Running Tests

```bash
cd test-data-demo
pip install pytest
pytest -v
```

**Note:** Tests will fail until the fixture data is generated!

## Data Models

### Customer
- `id`: string (UUID format)
- `name`: string
- `email`: string (valid email format)
- `membership_level`: string ("bronze", "silver", "gold", "platinum")
- `created_at`: string (ISO date format)

### Product
- `id`: string (UUID format)
- `name`: string
- `price`: float (positive)
- `category`: string
- `in_stock`: boolean
- `stock_quantity`: integer

### Order
- `id`: string (UUID format)
- `customer_id`: string (must match a customer)
- `items`: list of order items
  - `product_id`: string
  - `quantity`: integer (positive)
- `status`: string ("pending", "confirmed", "shipped", "delivered", "cancelled")
- `order_date`: string (ISO date format)
