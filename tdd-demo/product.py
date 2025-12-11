"""Product model for the shopping cart."""


class Product:
    """Represents a product that can be added to a shopping cart."""

    # Tax categories with different rates
    TAX_RATES = {
        "standard": 0.08,      # 8% - general merchandise
        "food": 0.02,          # 2% - groceries
        "luxury": 0.12,        # 12% - luxury items
        "exempt": 0.0,         # 0% - tax exempt
    }

    def __init__(self, name: str, price: float, category: str = "standard", weight: float = 0.5):
        """
        Initialize a product.

        Args:
            name: The product name
            price: The product price (must be non-negative)
            category: Tax category (standard, food, luxury, exempt)
            weight: Weight in pounds for shipping calculation
        """
        if price < 0:
            raise ValueError("Price cannot be negative")
        if category not in self.TAX_RATES:
            raise ValueError(f"Invalid category. Must be one of: {list(self.TAX_RATES.keys())}")
        if weight < 0:
            raise ValueError("Weight cannot be negative")
        
        self.name = name
        self.price = price
        self.category = category
        self.weight = weight

    @property
    def tax_rate(self) -> float:
        """Get the tax rate for this product's category."""
        return self.TAX_RATES[self.category]

    def __eq__(self, other):
        """Two products are equal if they have the same name."""
        if not isinstance(other, Product):
            return False
        return self.name == other.name

    def __hash__(self):
        """Hash based on name for use in dictionaries."""
        return hash(self.name)

    def __repr__(self):
        """Return string representation of the product."""
        return f"Product('{self.name}', {self.price}, '{self.category}')"
