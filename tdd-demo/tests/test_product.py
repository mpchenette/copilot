"""Tests for the Product class."""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from product import Product


class TestProduct:
    """Test suite for Product."""

    def test_create_product_with_name_and_price(self):
        """A product should have a name and price."""
        product = Product("Apple", 1.99)

        assert product.name == "Apple"
        assert product.price == 1.99

    def test_product_has_default_category(self):
        """Products default to 'standard' category."""
        product = Product("Apple", 1.99)
        assert product.category == "standard"

    def test_product_with_custom_category(self):
        """Products can have a custom tax category."""
        product = Product("Bread", 3.99, category="food")
        assert product.category == "food"

    def test_product_tax_rate_standard(self):
        """Standard products have 8% tax rate."""
        product = Product("Laptop", 999.99, category="standard")
        assert product.tax_rate == 0.08

    def test_product_tax_rate_food(self):
        """Food products have 2% tax rate."""
        product = Product("Milk", 4.99, category="food")
        assert product.tax_rate == 0.02

    def test_product_tax_rate_luxury(self):
        """Luxury products have 12% tax rate."""
        product = Product("Watch", 5000.00, category="luxury")
        assert product.tax_rate == 0.12

    def test_product_tax_rate_exempt(self):
        """Exempt products have 0% tax rate."""
        product = Product("Gift Card", 50.00, category="exempt")
        assert product.tax_rate == 0.0

    def test_product_price_cannot_be_negative(self):
        """Creating a product with negative price should raise ValueError."""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            Product("Apple", -1.00)

    def test_invalid_category_raises_error(self):
        """Invalid category should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid category"):
            Product("Item", 10.00, category="invalid")

    def test_product_has_default_weight(self):
        """Products have a default weight of 0.5 lbs."""
        product = Product("Apple", 1.99)
        assert product.weight == 0.5

    def test_product_with_custom_weight(self):
        """Products can have a custom weight."""
        product = Product("Dumbbell", 29.99, weight=10.0)
        assert product.weight == 10.0

    def test_product_equality_by_name(self):
        """Two products with same name are equal."""
        product1 = Product("Apple", 1.99)
        product2 = Product("Apple", 2.99)  # Different price

        assert product1 == product2

    def test_product_inequality_different_name(self):
        """Products with different names are not equal."""
        product1 = Product("Apple", 1.99)
        product2 = Product("Orange", 1.99)

        assert product1 != product2
