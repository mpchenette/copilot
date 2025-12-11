"""Test fixtures and data loading for tests."""

import pytest
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_loader import load_customers, load_products, load_orders


@pytest.fixture
def sample_customers():
    """Load sample customers from fixtures."""
    return load_customers()


@pytest.fixture
def sample_products():
    """Load sample products from fixtures."""
    return load_products()


@pytest.fixture
def sample_orders():
    """Load sample orders from fixtures."""
    return load_orders()


@pytest.fixture
def order_processor(sample_customers, sample_products):
    """Create an OrderProcessor with sample data."""
    from order_processor import OrderProcessor
    return OrderProcessor(sample_customers, sample_products)
