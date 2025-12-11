## are there tests in this app
- "are there any unit tests already in this app? if so can you run them to see if they pass? if they don't can you fix them?"

## Plan mode
- "I'm looking to write unit tests for this app but I need to be sure they are comprehensive and have as close to 100% test coverage as possible. Can you help me think through corner cases and uncommon scenarios I may need to test here? I want to log all of them in a file somewhere"
- save to file (i.e., do not start implementation, use other button)
- run prompt file

## execute / write tests / agent mode

## TDD (Agentic Demo)

### Setup
```bash
cd tdd-demo
pytest -v
```
You'll see: **17 passed, 18 failed, 7 skipped**

---

### 📝 Round 0: Write Your First Test (Live!)

**Show the TDD philosophy - test FIRST, then code**

1. Open `tests/test_cart.py` - show the commented-out first test
2. Uncomment or write this test live:
   ```python
   def test_empty_cart_has_zero_subtotal(self):
       """An empty cart should have subtotal of 0."""
       cart = ShoppingCart()
       assert cart.get_subtotal() == 0.0
   ```
3. Run: `pytest tests/test_cart.py::TestSubtotalWithBulkDiscounts::test_empty_cart_has_zero_subtotal -v`
4. Watch it fail! 🔴 `NotImplementedError: Implement using TDD!`
5. **Talking point:** "Now we have a failing test. In true TDD, we write the minimum code to pass."

---

### 🔴 Round 1: `get_subtotal()` with Bulk Discounts (9 more pre-written tests)

**The Challenge:** Implement tiered bulk discounts
- 10+ items: 15% off
- 5-9 items: 10% off
- 3-4 items: 5% off
- 1-2 items: no discount

**Demo Steps:**
1. **"I've already written the remaining tests. Let's see what else needs to pass."**
2. Run: `pytest tests/test_cart.py::TestSubtotalWithBulkDiscounts -v`
3. Show all 10 failing tests (including yours from Round 0)
4. Prompt: *"Fix the failing get_subtotal tests in cart.py"*
5. Watch AI implement the discount tier logic
6. Run tests → 🟢 10 tests pass!

---

### 🔴 Round 2: `get_tax()` with Category-Based Rates (9 failing tests)

**The Challenge:** Calculate tax per product category, on discounted prices
- Standard: 8%, Food: 2%, Luxury: 12%, Exempt: 0%
- Tax applies AFTER bulk discount

**Demo Steps:**
1. Run: `pytest tests/test_cart.py::TestTaxCalculation -v`
2. Show the 9 failing tests
3. Prompt: *"Fix the failing get_tax tests in cart.py"*
4. Watch AI implement category-based tax calculation
5. Run tests → 🟢 All 19 tests pass!

---

### Key Talking Points
- **Round 0** shows the TDD philosophy: test first
- **Rounds 1-2** show realistic workflow: tests exist, AI implements
- Real algorithms required (not one-liners!)
- AI reads test expectations and business rules from docstrings
- Round 2 depends on Round 1 (tax uses discounted subtotal)
- 7 more skipped tests for bonus round (shipping calculation)

## MCP

## Test data generation
- "can you generate test data for this app? In particular I need to popiulate the following files: `tests/fixtures/sample_customers.json`, `tests/fixtures/sample_products.json`, and `tests/fixtures/sample_orders.json`