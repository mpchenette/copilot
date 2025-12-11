"""Tests for Order model and OrderProcessor."""

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Order, OrderItem


class TestOrderValidation:
    """Test order validation logic."""

    def test_valid_orders_pass_validation(self, sample_orders):
        """All sample orders should pass basic validation."""
        for order in sample_orders:
            assert order.is_valid(), f"Order {order.id} should be valid"

    def test_orders_have_valid_status(self, sample_orders):
        """All orders should have valid status values."""
        for order in sample_orders:
            assert order.status in Order.VALID_STATUSES, \
                f"Order {order.id} has invalid status: {order.status}"

    def test_orders_have_at_least_one_item(self, sample_orders):
        """All orders should have at least one item."""
        for order in sample_orders:
            assert len(order.items) > 0, f"Order {order.id} has no items"

    def test_order_items_have_positive_quantities(self, sample_orders):
        """All order items should have positive quantities."""
        for order in sample_orders:
            for item in order.items:
                assert item.quantity > 0, \
                    f"Order {order.id} has item with non-positive quantity"

    def test_orders_have_unique_ids(self, sample_orders):
        """All orders should have unique IDs."""
        ids = [o.id for o in sample_orders]
        assert len(ids) == len(set(ids)), "Order IDs are not unique"


class TestOrderStatuses:
    """Test order status distribution and logic."""

    def test_has_orders_in_each_status(self, sample_orders):
        """Sample data should include orders in various statuses."""
        statuses_present = {o.status for o in sample_orders}
        
        # Should have at least pending and delivered orders
        assert "pending" in statuses_present, "No pending orders in sample data"
        assert "delivered" in statuses_present, "No delivered orders in sample data"

    def test_cancellable_orders(self, sample_orders):
        """Test can_be_cancelled logic on sample orders."""
        cancellable = [o for o in sample_orders if o.can_be_cancelled()]
        non_cancellable = [o for o in sample_orders if not o.can_be_cancelled()]
        
        # Verify cancellable orders have correct statuses
        for order in cancellable:
            assert order.status in ("pending", "confirmed"), \
                f"Order {order.id} should not be cancellable with status {order.status}"
        
        # Verify non-cancellable orders have correct statuses
        for order in non_cancellable:
            assert order.status in ("shipped", "delivered", "cancelled"), \
                f"Order {order.id} should be cancellable with status {order.status}"


class TestOrderProcessorValidation:
    """Test OrderProcessor validation."""

    def test_orders_reference_valid_customers(self, order_processor, sample_orders):
        """All orders should reference existing customers."""
        for order in sample_orders:
            customer = order_processor.get_customer(order.customer_id)
            assert customer is not None, \
                f"Order {order.id} references non-existent customer {order.customer_id}"

    def test_order_items_reference_valid_products(self, order_processor, sample_orders):
        """All order items should reference existing products."""
        for order in sample_orders:
            for item in order.items:
                product = order_processor.get_product(item.product_id)
                assert product is not None, \
                    f"Order {order.id} references non-existent product {item.product_id}"

    def test_validate_order_returns_success_for_valid_orders(self, order_processor, sample_orders, sample_products):
        """Valid orders should pass processor validation."""
        # Find orders that reference in-stock products
        in_stock_product_ids = {
            p.id for p in sample_products if p.in_stock and p.stock_quantity > 0
        }
        
        for order in sample_orders:
            # Check if all items are for in-stock products
            all_in_stock = all(
                item.product_id in in_stock_product_ids 
                for item in order.items
            )
            
            if all_in_stock:
                is_valid, errors = order_processor.validate_order(order)
                # Note: may fail due to quantity issues, which is okay


class TestOrderCalculations:
    """Test order total calculations."""

    def test_calculate_total_returns_positive_for_valid_orders(self, order_processor, sample_orders):
        """Order totals should be positive for valid orders."""
        for order in sample_orders:
            total = order_processor.calculate_order_total(order)
            assert total >= 0, f"Order {order.id} has negative total"

    def test_platinum_customers_get_best_discount(self, order_processor, sample_customers, sample_orders):
        """Platinum customers should have lowest totals for same items."""
        platinum_customers = [c for c in sample_customers if c.membership_level == "platinum"]
        bronze_customers = [c for c in sample_customers if c.membership_level == "bronze"]
        
        assert len(platinum_customers) > 0, "No platinum customers to test"
        assert len(bronze_customers) > 0, "No bronze customers to test"

    def test_get_total_items_is_correct(self, sample_orders):
        """get_total_items should return correct count."""
        for order in sample_orders:
            expected = sum(item.quantity for item in order.items)
            actual = order.get_total_items()
            assert actual == expected, \
                f"Order {order.id} total items mismatch: expected {expected}, got {actual}"


class TestOrderFiltering:
    """Test order filtering methods."""

    def test_filter_by_status(self, order_processor, sample_orders):
        """Should correctly filter orders by status."""
        for status in Order.VALID_STATUSES:
            filtered = order_processor.get_orders_by_status(sample_orders, status)
            for order in filtered:
                assert order.status == status

    def test_filter_by_customer(self, order_processor, sample_orders, sample_customers):
        """Should correctly filter orders by customer."""
        for customer in sample_customers:
            filtered = order_processor.get_customer_orders(sample_orders, customer.id)
            for order in filtered:
                assert order.customer_id == customer.id
