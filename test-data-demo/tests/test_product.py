"""Tests for Product model."""

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Product


class TestProductValidation:
    """Test product validation logic."""

    def test_valid_products_pass_validation(self, sample_products):
        """All sample products should pass validation."""
        for product in sample_products:
            assert product.is_valid(), f"Product {product.id} should be valid"

    def test_products_have_positive_prices(self, sample_products):
        """All products should have positive prices."""
        for product in sample_products:
            assert product.price > 0, f"Product {product.name} has non-positive price"

    def test_products_have_non_negative_stock(self, sample_products):
        """All products should have non-negative stock quantities."""
        for product in sample_products:
            assert product.stock_quantity >= 0, \
                f"Product {product.name} has negative stock"

    def test_products_have_unique_ids(self, sample_products):
        """All products should have unique IDs."""
        ids = [p.id for p in sample_products]
        assert len(ids) == len(set(ids)), "Product IDs are not unique"

    def test_products_have_categories(self, sample_products):
        """All products should have a category assigned."""
        for product in sample_products:
            assert product.category, f"Product {product.name} has no category"


class TestProductAvailability:
    """Test product availability logic."""

    def test_in_stock_products_have_positive_quantity(self, sample_products):
        """Products marked as in_stock should have positive quantity."""
        for product in sample_products:
            if product.in_stock:
                assert product.stock_quantity > 0, \
                    f"Product {product.name} is in_stock but has zero quantity"

    def test_out_of_stock_products_have_zero_quantity(self, sample_products):
        """Products not in_stock should have zero quantity."""
        for product in sample_products:
            if not product.in_stock:
                assert product.stock_quantity == 0, \
                    f"Product {product.name} is not in_stock but has quantity"

    def test_availability_check_works(self, sample_products):
        """is_available should return correct results."""
        for product in sample_products:
            if product.in_stock and product.stock_quantity >= 1:
                assert product.is_available(1), \
                    f"Product {product.name} should be available for quantity 1"
            
            # Should not be available for more than stock
            assert not product.is_available(product.stock_quantity + 1), \
                f"Product {product.name} should not be available for quantity exceeding stock"

    def test_has_mix_of_stock_statuses(self, sample_products):
        """Sample data should include both in-stock and out-of-stock products."""
        in_stock = [p for p in sample_products if p.in_stock]
        out_of_stock = [p for p in sample_products if not p.in_stock]
        
        assert len(in_stock) > 0, "No in-stock products in sample data"
        assert len(out_of_stock) > 0, "No out-of-stock products in sample data"


class TestProductCategories:
    """Test product categorization."""

    def test_has_multiple_categories(self, sample_products):
        """Sample data should have products in multiple categories."""
        categories = {p.category for p in sample_products}
        assert len(categories) >= 3, \
            f"Expected at least 3 categories, found: {categories}"

    def test_price_ranges_are_realistic(self, sample_products):
        """Products should have a range of prices."""
        prices = [p.price for p in sample_products]
        min_price = min(prices)
        max_price = max(prices)
        
        assert min_price < 50, "No low-priced items in sample data"
        assert max_price > 100, "No high-priced items in sample data"
