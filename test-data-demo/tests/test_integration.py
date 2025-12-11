"""Integration tests for the order processing system."""

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDataIntegrity:
    """Test that all fixture data works together correctly."""

    def test_all_fixtures_load_successfully(self, sample_customers, sample_products, sample_orders):
        """All fixture files should load without errors."""
        assert len(sample_customers) > 0, "No customers loaded"
        assert len(sample_products) > 0, "No products loaded"
        assert len(sample_orders) > 0, "No orders loaded"

    def test_minimum_data_requirements(self, sample_customers, sample_products, sample_orders):
        """Fixtures should have minimum required data for meaningful tests."""
        assert len(sample_customers) >= 5, "Need at least 5 customers for tests"
        assert len(sample_products) >= 10, "Need at least 10 products for tests"
        assert len(sample_orders) >= 8, "Need at least 8 orders for tests"

    def test_order_customer_references_are_valid(self, sample_customers, sample_orders):
        """All order customer_ids should reference actual customers."""
        customer_ids = {c.id for c in sample_customers}
        
        for order in sample_orders:
            assert order.customer_id in customer_ids, \
                f"Order {order.id} references unknown customer {order.customer_id}"

    def test_order_product_references_are_valid(self, sample_products, sample_orders):
        """All order product_ids should reference actual products."""
        product_ids = {p.id for p in sample_products}
        
        for order in sample_orders:
            for item in order.items:
                assert item.product_id in product_ids, \
                    f"Order {order.id} references unknown product {item.product_id}"


class TestEndToEndScenarios:
    """End-to-end scenario tests."""

    def test_process_valid_order_workflow(self, order_processor, sample_orders, sample_products):
        """Test complete order processing workflow."""
        # Find an order with in-stock items
        in_stock_ids = {p.id for p in sample_products if p.in_stock and p.stock_quantity >= 5}
        
        valid_order = None
        for order in sample_orders:
            if all(item.product_id in in_stock_ids and item.quantity <= 5 for item in order.items):
                valid_order = order
                break
        
        if valid_order:
            is_valid, errors = order_processor.validate_order(valid_order)
            # Order should be valid if products have sufficient stock

    def test_low_stock_detection(self, order_processor, sample_products):
        """Test detection of low stock products."""
        low_stock = order_processor.get_low_stock_products(threshold=10)
        
        # Verify all returned products are actually low stock
        for product in low_stock:
            assert product.stock_quantity <= 10

    def test_customer_order_history(self, order_processor, sample_orders, sample_customers):
        """Test retrieving customer order history."""
        # Find a customer with orders
        for customer in sample_customers:
            orders = order_processor.get_customer_orders(sample_orders, customer.id)
            for order in orders:
                assert order.customer_id == customer.id


class TestEdgeCases:
    """Test edge cases in the data."""

    def test_has_high_value_order(self, order_processor, sample_orders):
        """Sample data should include at least one high-value order."""
        totals = [order_processor.calculate_order_total(o) for o in sample_orders]
        max_total = max(totals)
        assert max_total >= 100, "No high-value orders in sample data"

    def test_has_single_item_order(self, sample_orders):
        """Sample data should include orders with single items."""
        single_item_orders = [o for o in sample_orders if len(o.items) == 1]
        assert len(single_item_orders) > 0, "No single-item orders in sample data"

    def test_has_multi_item_order(self, sample_orders):
        """Sample data should include orders with multiple items."""
        multi_item_orders = [o for o in sample_orders if len(o.items) > 1]
        assert len(multi_item_orders) > 0, "No multi-item orders in sample data"

    def test_has_cancelled_order(self, sample_orders):
        """Sample data should include at least one cancelled order."""
        cancelled = [o for o in sample_orders if o.status == "cancelled"]
        assert len(cancelled) > 0, "No cancelled orders in sample data"
