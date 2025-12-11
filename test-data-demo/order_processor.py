"""Order processing logic."""

from typing import Dict, List, Optional, Tuple
from models import Customer, Product, Order, OrderItem


class OrderProcessor:
    """Handles order validation and processing."""

    def __init__(self, customers: List[Customer], products: List[Product]):
        self.customers = {c.id: c for c in customers}
        self.products = {p.id: p for p in products}

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Retrieve a customer by ID."""
        return self.customers.get(customer_id)

    def get_product(self, product_id: str) -> Optional[Product]:
        """Retrieve a product by ID."""
        return self.products.get(product_id)

    def validate_order(self, order: Order) -> Tuple[bool, List[str]]:
        """
        Validate an order and return validation result with error messages.
        """
        errors = []

        if not order.is_valid():
            errors.append("Order has invalid structure")
            return False, errors

        # Validate customer exists
        customer = self.get_customer(order.customer_id)
        if not customer:
            errors.append(f"Customer {order.customer_id} not found")

        # Validate each item
        for item in order.items:
            product = self.get_product(item.product_id)
            if not product:
                errors.append(f"Product {item.product_id} not found")
            elif not product.is_available(item.quantity):
                errors.append(
                    f"Product {product.name} has insufficient stock "
                    f"(requested: {item.quantity}, available: {product.stock_quantity})"
                )

        return len(errors) == 0, errors

    def calculate_order_total(self, order: Order) -> float:
        """Calculate the total price for an order including discounts."""
        if not order.is_valid():
            return 0.0

        subtotal = 0.0
        for item in order.items:
            product = self.get_product(item.product_id)
            if product:
                subtotal += product.price * item.quantity

        # Apply customer discount
        customer = self.get_customer(order.customer_id)
        if customer:
            discount_rate = customer.get_discount_rate()
            subtotal *= (1 - discount_rate)

        return round(subtotal, 2)

    def process_order(self, order: Order) -> Tuple[bool, str]:
        """
        Process an order: validate, calculate total, and update stock.
        Returns success status and message.
        """
        is_valid, errors = self.validate_order(order)
        if not is_valid:
            return False, f"Order validation failed: {'; '.join(errors)}"

        # Update stock quantities
        for item in order.items:
            product = self.get_product(item.product_id)
            if product:
                product.stock_quantity -= item.quantity
                if product.stock_quantity == 0:
                    product.in_stock = False

        total = self.calculate_order_total(order)
        return True, f"Order processed successfully. Total: ${total:.2f}"

    def get_orders_by_status(self, orders: List[Order], status: str) -> List[Order]:
        """Filter orders by status."""
        return [o for o in orders if o.status == status]

    def get_customer_orders(self, orders: List[Order], customer_id: str) -> List[Order]:
        """Get all orders for a specific customer."""
        return [o for o in orders if o.customer_id == customer_id]

    def get_low_stock_products(self, threshold: int = 5) -> List[Product]:
        """Get products with stock below the threshold."""
        return [
            p for p in self.products.values()
            if p.stock_quantity <= threshold
        ]
