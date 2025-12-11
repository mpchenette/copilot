# 🛒 Shopping Cart Pricing Engine - TDD Demo

A hands-on Test-Driven Development demonstration featuring a realistic pricing engine with bulk discounts, category-based taxes, and shipping calculations.

## Quick Start

```bash
cd tdd-demo
pytest -v
```

You'll see: **18 passed, 10 failed, 7 skipped**

## The Challenge

The `ShoppingCart` needs a **pricing engine** with real business logic:

### Round 1: `get_subtotal()` with Bulk Discounts
- Calculate subtotal from all items (price × quantity)
- Apply tiered bulk discounts based on total items:
  - **10+ items**: 15% off
  - **5-9 items**: 10% off
  - **3-4 items**: 5% off
  - **1-2 items**: no discount

### Round 2: `get_tax()` with Category-Based Rates
- Each product has a tax category with different rates:
  - **Standard**: 8% (general merchandise)
  - **Food**: 2% (groceries)
  - **Luxury**: 12% (premium items)
  - **Exempt**: 0% (gift cards, etc.)
- Tax calculated on **discounted** prices (after bulk discount)

### Bonus Round: `get_shipping()`
- Free shipping over $50
- Base rate: $5.99
- Heavy item surcharge: +$3.00 per item ≥ 5 lbs

## Demo Flow

### 🔴 Round 1: Subtotal (10 failing tests)
```bash
pytest tests/test_cart.py::TestSubtotalWithBulkDiscounts -v
```
1. Show failing tests
2. Prompt: *"Fix the failing get_subtotal tests"*
3. Watch AI implement the discount logic
4. Run tests → 🟢 Green!

### 🔴 Round 2: Tax (9 failing tests)
```bash
pytest tests/test_cart.py::TestTaxCalculation -v
```
1. Show failing tests  
2. Prompt: *"Fix the failing get_tax tests"*
3. Watch AI implement category-based tax calculation
4. Run tests → 🟢 Green!

## What Makes This Demo Impressive

- **Real algorithm required**: Can't solve with one-liners
- **Business rules to implement**: Tiered discounts, tax rates
- **Edge cases covered**: Empty cart, rounding, mixed categories
- **Progressive complexity**: Round 2 depends on Round 1
- **Relatable domain**: Everyone understands shopping carts

## Project Structure

```
tdd-demo/
├── README.md
├── product.py        # Product with categories and weights
├── cart.py           # Shopping cart with pricing engine
├── pytest.ini
└── tests/
    ├── test_product.py   # Product tests (passing)
    └── test_cart.py      # Cart tests (some failing!)
```
