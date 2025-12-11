"""Shopping cart with pricing engine."""

from product import Product


class CartItem:
    """Represents a product with quantity in the cart."""

    def __init__(self, product: Product, quantity: int = 1):
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        self.product = product
        self.quantity = quantity

    @property
    def line_total(self) -> float:
        """Calculate total for this line item (price * quantity)."""
        return self.product.price * self.quantity

    def __repr__(self):
        return f"CartItem({self.product.name}, qty={self.quantity})"


class ShoppingCart:
    """
    A shopping cart with full pricing engine.
    
    Features:
    - Quantity management (adding same product increases quantity)
    - Tiered bulk discounts (buy more, save more)
    - Category-based tax calculation
    - Weight-based shipping with free shipping threshold
    - Coupon code support
    """

    # Shipping constants
    BASE_SHIPPING = 5.99
    FREE_SHIPPING_THRESHOLD = 50.00
    HEAVY_ITEM_SURCHARGE = 3.00
    HEAVY_WEIGHT_THRESHOLD = 5.0  # pounds

    # Bulk discount tiers: (min_quantity, discount_percent)
    BULK_DISCOUNT_TIERS = [
        (10, 0.15),  # 10+ items: 15% off
        (5, 0.10),   # 5-9 items: 10% off
        (3, 0.05),   # 3-4 items: 5% off
    ]

    # Valid coupon codes: code -> (discount_type, value, min_purchase)
    COUPON_CODES = {
        "SAVE10": ("percent", 10, 0),           # 10% off, no minimum
        "SAVE20": ("percent", 20, 50),          # 20% off, $50 minimum
        "FLAT15": ("fixed", 15, 30),            # $15 off, $30 minimum
        "FREESHIP": ("shipping", 100, 25),      # Free shipping, $25 minimum
    }

    def __init__(self):
        """Initialize an empty shopping cart."""
        self._items: dict[str, CartItem] = {}  # keyed by product name
        self._applied_coupon: str | None = None

    def add_item(self, product: Product, quantity: int = 1) -> None:
        """
        Add a product to the cart.
        If product already exists, increase its quantity.
        """
        if product.name in self._items:
            self._items[product.name].quantity += quantity
        else:
            self._items[product.name] = CartItem(product, quantity)

    def get_item_count(self) -> int:
        """Return the total number of items (sum of all quantities)."""
        return sum(item.quantity for item in self._items.values())

    def get_unique_item_count(self) -> int:
        """Return the number of unique products in the cart."""
        return len(self._items)

    def is_empty(self) -> bool:
        """Return True if the cart is empty."""
        return len(self._items) == 0

    # ============================================================
    # TDD DEMO ROUND 1: Subtotal with Bulk Discounts
    # ============================================================

    def get_subtotal(self) -> float:
        """
        Calculate subtotal with bulk discounts applied.
        
        Business Rules:
        - Sum up (price * quantity) for each item
        - Apply bulk discount based on TOTAL items in cart:
          - 10+ items: 15% off
          - 5-9 items: 10% off  
          - 3-4 items: 5% off
          - 1-2 items: no discount
        - Round to 2 decimal places
        
        TODO: Implement using TDD!
        """
        raise NotImplementedError("Implement using TDD!")

    def _get_bulk_discount_rate(self) -> float:
        """
        Get the bulk discount rate based on total item count.
        Helper method - implement this too!
        """
        raise NotImplementedError("Implement using TDD!")

    # ============================================================
    # TDD DEMO ROUND 2: Tax Calculation
    # ============================================================

    def get_tax(self) -> float:
        """
        Calculate tax based on each product's category.
        
        Business Rules:
        - Each product has a tax category (standard=8%, food=2%, luxury=12%, exempt=0%)
        - Tax is calculated on the DISCOUNTED subtotal for each item
        - Apply bulk discount to each line item proportionally before calculating tax
        - Round to 2 decimal places
        
        Example:
        - Cart has 5 items total (10% bulk discount applies)
        - 3 standard items @ $10 = $30 -> $27 after discount -> $2.16 tax
        - 2 food items @ $5 = $10 -> $9 after discount -> $0.18 tax
        - Total tax = $2.34
        
        TODO: Implement using TDD!
        """
        raise NotImplementedError("Implement using TDD!")

    # ============================================================
    # TDD DEMO ROUND 3 (BONUS): Shipping Calculation
    # ============================================================

    def get_shipping(self) -> float:
        """
        Calculate shipping cost.
        
        Business Rules:
        - Free shipping if subtotal >= $50
        - Otherwise, base shipping is $5.99
        - Add $3.00 surcharge for each item weighing 5+ pounds
        - If FREESHIP coupon is applied, shipping is $0
        - Empty cart = $0 shipping
        
        TODO: Implement using TDD!
        """
        raise NotImplementedError("Implement using TDD!")

    # ============================================================
    # ALREADY IMPLEMENTED (for demo setup)
    # ============================================================

    def apply_coupon(self, code: str) -> bool:
        """
        Apply a coupon code to the cart.
        Returns True if coupon was valid and applied.
        """
        code = code.upper()
        if code not in self.COUPON_CODES:
            return False
        
        discount_type, value, min_purchase = self.COUPON_CODES[code]
        
        # Check minimum purchase requirement
        raw_subtotal = sum(item.line_total for item in self._items.values())
        if raw_subtotal < min_purchase:
            return False
        
        self._applied_coupon = code
        return True

    def get_coupon_discount(self) -> float:
        """Calculate the discount from the applied coupon."""
        if not self._applied_coupon:
            return 0.0
        
        discount_type, value, _ = self.COUPON_CODES[self._applied_coupon]
        
        if discount_type == "percent":
            # Percentage off subtotal
            return round(self.get_subtotal() * (value / 100), 2)
        elif discount_type == "fixed":
            # Fixed dollar amount off
            return min(value, self.get_subtotal())  # Can't exceed subtotal
        elif discount_type == "shipping":
            # Shipping discount handled in get_shipping()
            return 0.0
        
        return 0.0

    def get_total(self) -> float:
        """
        Calculate final total: subtotal + tax + shipping - coupon discount.
        Note: Requires get_subtotal(), get_tax(), and get_shipping() to work.
        """
        subtotal = self.get_subtotal()
        tax = self.get_tax()
        shipping = self.get_shipping()
        coupon_discount = self.get_coupon_discount()
        
        return round(subtotal + tax + shipping - coupon_discount, 2)
