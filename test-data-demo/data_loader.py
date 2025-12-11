"""Utilities for loading test data from JSON fixtures."""

import json
import os
from typing import List
from models import Customer, Product, Order, OrderItem


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "tests", "fixtures")


def load_customers(filepath: str = None) -> List[Customer]:
    """Load customers from a JSON file."""
    if filepath is None:
        filepath = os.path.join(FIXTURES_DIR, "sample_customers.json")
    
    with open(filepath, "r") as f:
        data = json.load(f)
    
    return [
        Customer(
            id=c["id"],
            name=c["name"],
            email=c["email"],
            membership_level=c["membership_level"],
            created_at=c["created_at"]
        )
        for c in data
    ]


def load_products(filepath: str = None) -> List[Product]:
    """Load products from a JSON file."""
    if filepath is None:
        filepath = os.path.join(FIXTURES_DIR, "sample_products.json")
    
    with open(filepath, "r") as f:
        data = json.load(f)
    
    return [
        Product(
            id=p["id"],
            name=p["name"],
            price=p["price"],
            category=p["category"],
            in_stock=p["in_stock"],
            stock_quantity=p["stock_quantity"]
        )
        for p in data
    ]


def load_orders(filepath: str = None) -> List[Order]:
    """Load orders from a JSON file."""
    if filepath is None:
        filepath = os.path.join(FIXTURES_DIR, "sample_orders.json")
    
    with open(filepath, "r") as f:
        data = json.load(f)
    
    orders = []
    for o in data:
        items = [
            OrderItem(product_id=i["product_id"], quantity=i["quantity"])
            for i in o["items"]
        ]
        orders.append(
            Order(
                id=o["id"],
                customer_id=o["customer_id"],
                items=items,
                status=o["status"],
                order_date=o["order_date"]
            )
        )
    return orders
