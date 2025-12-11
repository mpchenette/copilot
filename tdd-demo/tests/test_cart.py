"""Tests for the ShoppingCart pricing engine."""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cart import ShoppingCart, CartItem
from product import Product


class TestCartBasics:
    """Basic cart tests - these already pass!"""

    def test_new_cart_is_empty(self):
        """A new shopping cart should be empty."""
        cart = ShoppingCart()
        assert cart.is_empty() is True
        assert cart.get_item_count() == 0

    def test_add_single_item(self):
        """Adding an item should increase the count."""
        cart = ShoppingCart()
        cart.add_item(Product("Apple", 1.99))
        assert cart.get_item_count() == 1

    def test_add_same_product_increases_quantity(self):
        """Adding the same product should increase quantity, not add new item."""
        cart = ShoppingCart()
        apple = Product("Apple", 1.99)
        
        cart.add_item(apple, quantity=2)
        cart.add_item(apple, quantity=3)
        
        assert cart.get_unique_item_count() == 1  # Still one unique product
        assert cart.get_item_count() == 5          # But 5 total items

    def test_add_item_with_quantity(self):
        """Can add multiple of same item at once."""
        cart = ShoppingCart()
        cart.add_item(Product("Apple", 1.99), quantity=5)
        assert cart.get_item_count() == 5


class TestSubtotalWithBulkDiscounts:
    """
    🔴 TDD DEMO ROUND 1: Subtotal Calculation with Bulk Discounts
    
    These tests are FAILING! Implement get_subtotal() to make them pass.
    
    Business Rules:
    - 10+ items: 15% off
    - 5-9 items: 10% off
    - 3-4 items: 5% off
    - 1-2 items: no discount
    """

    # ⬇️ WRITE THIS TEST LIVE DURING DEMO ⬇️
    # def test_empty_cart_has_zero_subtotal(self):
    #     """An empty cart should have subtotal of 0."""
    #     cart = ShoppingCart()
    #     assert cart.get_subtotal() == 0.0

    def test_single_item_no_discount(self):
        """Single item gets no bulk discount."""
        cart = ShoppingCart()
        cart.add_item(Product("Laptop", 100.00))
        
        # 1 item = no discount, subtotal = $100
        assert cart.get_subtotal() == 100.00

    def test_two_items_no_discount(self):
        """Two items still get no bulk discount."""
        cart = ShoppingCart()
        cart.add_item(Product("Book", 25.00), quantity=2)
        
        # 2 items = no discount, subtotal = $50
        assert cart.get_subtotal() == 50.00

    def test_three_items_five_percent_discount(self):
        """3-4 items get 5% bulk discount."""
        cart = ShoppingCart()
        cart.add_item(Product("Shirt", 20.00), quantity=3)
        
        # 3 items @ $20 = $60, minus 5% = $57
        assert cart.get_subtotal() == 57.00

    def test_four_items_five_percent_discount(self):
        """4 items still in 5% discount tier."""
        cart = ShoppingCart()
        cart.add_item(Product("Mug", 10.00), quantity=4)
        
        # 4 items @ $10 = $40, minus 5% = $38
        assert cart.get_subtotal() == 38.00

    def test_five_items_ten_percent_discount(self):
        """5-9 items get 10% bulk discount."""
        cart = ShoppingCart()
        cart.add_item(Product("Pen", 5.00), quantity=5)
        
        # 5 items @ $5 = $25, minus 10% = $22.50
        assert cart.get_subtotal() == 22.50

    def test_nine_items_ten_percent_discount(self):
        """9 items still in 10% discount tier."""
        cart = ShoppingCart()
        cart.add_item(Product("Notebook", 8.00), quantity=9)
        
        # 9 items @ $8 = $72, minus 10% = $64.80
        assert cart.get_subtotal() == 64.80

    def test_ten_items_fifteen_percent_discount(self):
        """10+ items get 15% bulk discount."""
        cart = ShoppingCart()
        cart.add_item(Product("Sticker", 2.00), quantity=10)
        
        # 10 items @ $2 = $20, minus 15% = $17
        assert cart.get_subtotal() == 17.00

    def test_bulk_discount_with_mixed_products(self):
        """Bulk discount applies to total item count across all products."""
        cart = ShoppingCart()
        cart.add_item(Product("Apple", 1.00), quantity=3)
        cart.add_item(Product("Banana", 0.50), quantity=2)
        
        # 5 total items = 10% discount
        # Raw: (3 * $1) + (2 * $0.50) = $4.00
        # After 10% off: $3.60
        assert cart.get_subtotal() == 3.60

    def test_subtotal_rounds_to_two_decimals(self):
        """Subtotal should be rounded to 2 decimal places."""
        cart = ShoppingCart()
        # Create a scenario that would produce more than 2 decimals
        cart.add_item(Product("Widget", 3.33), quantity=3)
        
        # 3 items @ $3.33 = $9.99, minus 5% = $9.4905 -> rounds to $9.49
        assert cart.get_subtotal() == 9.49


class TestTaxCalculation:
    """
    🔴 TDD DEMO ROUND 2: Tax Calculation by Category
    
    These tests are FAILING! Implement get_tax() to make them pass.
    
    Tax rates by category:
    - standard: 8%
    - food: 2%
    - luxury: 12%
    - exempt: 0%
    
    Tax is calculated on the DISCOUNTED price!
    """

    def test_empty_cart_has_zero_tax(self):
        """Empty cart has no tax."""
        cart = ShoppingCart()
        assert cart.get_tax() == 0.0

    def test_standard_tax_rate(self):
        """Standard category items have 8% tax."""
        cart = ShoppingCart()
        cart.add_item(Product("Laptop", 100.00, category="standard"))
        
        # 1 item = no bulk discount
        # Tax: $100 * 8% = $8.00
        assert cart.get_tax() == 8.00

    def test_food_tax_rate(self):
        """Food category items have 2% tax."""
        cart = ShoppingCart()
        cart.add_item(Product("Bread", 5.00, category="food"))
        
        # 1 item = no bulk discount
        # Tax: $5 * 2% = $0.10
        assert cart.get_tax() == 0.10

    def test_luxury_tax_rate(self):
        """Luxury category items have 12% tax."""
        cart = ShoppingCart()
        cart.add_item(Product("Watch", 200.00, category="luxury"))
        
        # 1 item = no bulk discount
        # Tax: $200 * 12% = $24.00
        assert cart.get_tax() == 24.00

    def test_exempt_has_no_tax(self):
        """Exempt category items have 0% tax."""
        cart = ShoppingCart()
        cart.add_item(Product("Gift Card", 50.00, category="exempt"))
        
        assert cart.get_tax() == 0.0

    def test_mixed_categories_tax(self):
        """Tax calculated correctly for mixed categories."""
        cart = ShoppingCart()
        cart.add_item(Product("Laptop", 100.00, category="standard"))  # 8%
        cart.add_item(Product("Bread", 10.00, category="food"))        # 2%
        
        # 2 items = no bulk discount
        # Standard: $100 * 8% = $8.00
        # Food: $10 * 2% = $0.20
        # Total tax: $8.20
        assert cart.get_tax() == 8.20

    def test_tax_calculated_on_discounted_subtotal(self):
        """Tax should be calculated AFTER bulk discount is applied."""
        cart = ShoppingCart()
        cart.add_item(Product("Book", 10.00, category="standard"), quantity=5)
        
        # 5 items = 10% bulk discount
        # Raw: $50, After discount: $45
        # Tax: $45 * 8% = $3.60
        assert cart.get_tax() == 3.60

    def test_tax_with_mixed_categories_and_bulk_discount(self):
        """Complex scenario: mixed categories with bulk discount."""
        cart = ShoppingCart()
        cart.add_item(Product("Gadget", 20.00, category="standard"), quantity=3)  # 8%
        cart.add_item(Product("Snacks", 10.00, category="food"), quantity=2)      # 2%
        
        # 5 total items = 10% bulk discount
        # Gadgets: $60 -> $54 after discount -> $54 * 8% = $4.32
        # Snacks: $20 -> $18 after discount -> $18 * 2% = $0.36
        # Total tax: $4.68
        assert cart.get_tax() == 4.68

    def test_tax_rounds_to_two_decimals(self):
        """Tax should be rounded to 2 decimal places."""
        cart = ShoppingCart()
        cart.add_item(Product("Item", 33.33, category="standard"))
        
        # $33.33 * 8% = $2.6664 -> rounds to $2.67
        assert cart.get_tax() == 2.67


class TestShippingCalculation:
    """
    🔴 TDD DEMO ROUND 3 (BONUS): Shipping Calculation
    
    These tests are SKIPPED. Enable them for an extended demo!
    
    Rules:
    - Free shipping if subtotal >= $50
    - Base shipping: $5.99
    - Heavy item surcharge: +$3.00 per item >= 5 lbs
    """

    @pytest.mark.skip(reason="Bonus round - enable when ready")
    def test_empty_cart_no_shipping(self):
        """Empty cart has no shipping cost."""
        cart = ShoppingCart()
        assert cart.get_shipping() == 0.0

    @pytest.mark.skip(reason="Bonus round - enable when ready")
    def test_base_shipping_under_threshold(self):
        """Orders under $50 pay base shipping."""
        cart = ShoppingCart()
        cart.add_item(Product("Book", 20.00))
        
        assert cart.get_shipping() == 5.99

    @pytest.mark.skip(reason="Bonus round - enable when ready")
    def test_free_shipping_at_threshold(self):
        """Orders at exactly $50 get free shipping."""
        cart = ShoppingCart()
        cart.add_item(Product("Item", 50.00))
        
        assert cart.get_shipping() == 0.0

    @pytest.mark.skip(reason="Bonus round - enable when ready")
    def test_free_shipping_over_threshold(self):
        """Orders over $50 get free shipping."""
        cart = ShoppingCart()
        cart.add_item(Product("Laptop", 500.00))
        
        assert cart.get_shipping() == 0.0

    @pytest.mark.skip(reason="Bonus round - enable when ready")
    def test_heavy_item_surcharge(self):
        """Heavy items (5+ lbs) add $3 surcharge each."""
        cart = ShoppingCart()
        cart.add_item(Product("Light Item", 10.00, weight=1.0))
        cart.add_item(Product("Heavy Item", 15.00, weight=6.0))
        
        # Under $50 threshold, so base shipping applies
        # Plus $3 for the heavy item
        # $5.99 + $3.00 = $8.99
        assert cart.get_shipping() == 8.99

    @pytest.mark.skip(reason="Bonus round - enable when ready")
    def test_multiple_heavy_items_surcharge(self):
        """Each heavy item adds its own surcharge."""
        cart = ShoppingCart()
        cart.add_item(Product("Dumbbell", 10.00, weight=10.0), quantity=2)
        
        # Under $50, base shipping + 2 heavy surcharges
        # $5.99 + $3.00 + $3.00 = $11.99
        assert cart.get_shipping() == 11.99

    @pytest.mark.skip(reason="Bonus round - enable when ready")
    def test_heavy_items_still_charged_over_threshold(self):
        """Heavy item surcharge applies even with free shipping threshold."""
        cart = ShoppingCart()
        cart.add_item(Product("Heavy Expensive", 100.00, weight=8.0))
        
        # Over $50 so free base shipping, but still pay heavy surcharge
        assert cart.get_shipping() == 3.00
