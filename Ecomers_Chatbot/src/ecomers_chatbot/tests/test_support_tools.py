"""
Tests for escalate_to_human - Milestone 16 test table row: 'Human'.
"""

import re
from ecomers_chatbot.tools.Support_tools import escalate_to_human


def test_escalation_creates_a_ticket():
    result = escalate_to_human.invoke("customer explicitly requested a human")
    assert result.startswith("SUCCESS")
    assert "ticket_id=TKT-" in result
    assert "status=created" in result


def test_ticket_ids_increment_across_calls():
    first = escalate_to_human.invoke("reason A")
    second = escalate_to_human.invoke("reason B")

    first_id = re.search(r"TKT-(\d+)", first).group(1)
    second_id = re.search(r"TKT-(\d+)", second).group(1)

    assert int(second_id) == int(first_id) + 1