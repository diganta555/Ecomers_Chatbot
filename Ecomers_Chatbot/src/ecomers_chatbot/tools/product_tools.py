"""
Product information tool.

Same no-hallucination principle as the order tools: price, stock, and
warranty are facts that must come from data/products.py, never from
the LLM's imagination.
"""

from langchain_core.tools import tool
from ecomers_chatbot.data.products import find_product


@tool
def get_product_information(product_name: str) -> str:
    """
    Look up authoritative information about a product by name
    (e.g. 'MacBook Air M3', 'Sony headphones'). Returns name, category,
    price, stock status, description, and warranty, or a clear
    not-found message if no matching product exists. Always use this
    tool for product questions instead of guessing specs or prices.
    """
    product = find_product(product_name)

    if product is None:
        return f"NOT_FOUND: No product matching '{product_name}' was found in the catalog."

    return (
        f"FOUND: {product['name']} - category: {product['category']}, "
        f"price: ${product['price']}, stock: {product['stock']}, "
        f"warranty: {product['warranty']}. {product['description']}"
    )