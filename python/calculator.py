class Calculator:
    """A simple calculator class with basic arithmetic operations."""
    
    def add(self, a, b):
        """Add two numbers."""
        return a + b
    
    def subtract(self, a, b):
        """Subtract b from a."""
        return a - b
    
    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b
    
    def divide(self, a, b):
        """Divide a by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, a, b):
        """Raise a to the power of b."""
        return a ** b
    
    def square_root(self, a):
        """Calculate the square root of a number."""
        if a < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return a ** 0.5