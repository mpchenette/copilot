"""Tests for Customer model."""

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Customer


class TestCustomerValidation:
    """Test customer validation logic."""

    def test_valid_customers_pass_validation(self, sample_customers):
        """All sample customers should pass validation."""
        for customer in sample_customers:
            assert customer.is_valid(), f"Customer {customer.id} should be valid"

    def test_customer_has_valid_email_format(self, sample_customers):
        """All customers should have valid email addresses."""
        for customer in sample_customers:
            assert "@" in customer.email, f"Customer {customer.name} has invalid email"
            assert "." in customer.email.split("@")[1], f"Customer {customer.name} has invalid email domain"

    def test_customer_membership_levels_are_valid(self, sample_customers):
        """All customers should have valid membership levels."""
        valid_levels = Customer.VALID_MEMBERSHIP_LEVELS
        for customer in sample_customers:
            assert customer.membership_level in valid_levels, \
                f"Customer {customer.name} has invalid membership level: {customer.membership_level}"

    def test_customers_have_unique_ids(self, sample_customers):
        """All customers should have unique IDs."""
        ids = [c.id for c in sample_customers]
        assert len(ids) == len(set(ids)), "Customer IDs are not unique"

    def test_customers_have_unique_emails(self, sample_customers):
        """All customers should have unique emails."""
        emails = [c.email for c in sample_customers]
        assert len(emails) == len(set(emails)), "Customer emails are not unique"


class TestCustomerDiscounts:
    """Test customer discount rate logic."""

    def test_discount_rates_by_membership(self, sample_customers):
        """Verify discount rates are correct for each membership level."""
        expected_discounts = {
            "bronze": 0.0,
            "silver": 0.05,
            "gold": 0.10,
            "platinum": 0.15
        }
        
        for customer in sample_customers:
            expected = expected_discounts[customer.membership_level]
            actual = customer.get_discount_rate()
            assert actual == expected, \
                f"Customer {customer.name} ({customer.membership_level}) has wrong discount rate"

    def test_has_customers_at_each_membership_level(self, sample_customers):
        """Sample data should include at least one customer at each level."""
        levels_present = {c.membership_level for c in sample_customers}
        for level in Customer.VALID_MEMBERSHIP_LEVELS:
            assert level in levels_present, \
                f"No sample customer with membership level '{level}'"
