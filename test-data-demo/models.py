"""Data models for the order processing system."""

from dataclasses import dataclass
from typing import List
import re
from datetime import datetime


@dataclass
class Customer:
    id: str
    name: str
    email: str
    membership_level: str
    created_at: str

    VALID_MEMBERSHIP_LEVELS = ("bronze", "silver", "gold", "platinum")

    def is_valid(self) -> bool:
        """Validate the customer data."""
        if not self.id or not self.name:
            return False
        if not self._is_valid_email(self.email):
            return False
        if self.membership_level not in self.VALID_MEMBERSHIP_LEVELS:
            return False
        return True

    def _is_valid_email(self, email: str) -> bool:
        """Check if email format is valid."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def get_discount_rate(self) -> float:
        """Get discount rate based on membership level."""
        discounts = {
            "bronze": 0.0,
            "silver": 0.05,
            "gold": 0.10,
            "platinum": 0.15
        }
        return discounts.get(self.membership_level, 0.0)


@dataclass
class Product:
    id: str
    name: str
    price: float
    category: str
    in_stock: bool
    stock_quantity: int

    def is_valid(self) -> bool:
        """Validate the product data."""
        if not self.id or not self.name:
            return False
        if self.price <= 0:
            return False
        if self.stock_quantity < 0:
            return False
        return True

    def is_available(self, quantity: int) -> bool:
        """Check if the requested quantity is available."""
        return self.in_stock and self.stock_quantity >= quantity


@dataclass
class OrderItem:
    product_id: str
    quantity: int

    def is_valid(self) -> bool:
        """Validate the order item."""
        return bool(self.product_id) and self.quantity > 0


@dataclass
class Order:
    id: str
    customer_id: str
    items: List[OrderItem]
    status: str
    order_date: str

    VALID_STATUSES = ("pending", "confirmed", "shipped", "delivered", "cancelled")

    def is_valid(self) -> bool:
        """Validate the order data."""
        if not self.id or not self.customer_id:
            return False
        if not self.items:
            return False
        if self.status not in self.VALID_STATUSES:
            return False
        if not all(item.is_valid() for item in self.items):
            return False
        return True

    def can_be_cancelled(self) -> bool:
        """Check if the order can be cancelled."""
        return self.status in ("pending", "confirmed")

    def get_total_items(self) -> int:
        """Get total number of items in the order."""
        return sum(item.quantity for item in self.items)
