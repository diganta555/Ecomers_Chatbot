"""
Shared pytest fixtures.

The refund and cancellation tools MUTATE the module-level ORDERS dict
in data/orders.py (that's how they simulate a real database write).
Without resetting between tests, refunding ORD-1001 in one test would
leave it permanently "Refunded" for every test that runs after it.

This autouse fixture snapshots ORDERS before each test and restores it
afterward, so every test starts from the same known mock data
regardless of run order.
"""

import copy
import pytest

from ecomers_chatbot.data.orders import ORDERS


@pytest.fixture(autouse=True)
def reset_orders():
    original = copy.deepcopy(ORDERS)
    yield
    ORDERS.clear()
    ORDERS.update(original)