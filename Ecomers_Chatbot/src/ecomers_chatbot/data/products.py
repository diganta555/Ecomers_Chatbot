"""
Mock product database - single source of truth for product facts,
same pattern as data/orders.py.
"""

PRODUCTS = {
    "iphone 15": {
        "name": "iPhone 15",
        "category": "Smartphone",
        "price": 699,
        "stock": "Available",
        "description": "Apple's latest-generation smartphone.",
        "warranty": "1 year",
    },
    "iphone 15 pro": {
        "name": "iPhone 15 Pro",
        "category": "Smartphone",
        "price": 999,
        "stock": "Available",
        "description": "Apple's pro-tier smartphone with a titanium frame and A17 Pro chip.",
        "warranty": "1 year",
    },
    "samsung galaxy s25": {
        "name": "Samsung Galaxy S25",
        "category": "Smartphone",
        "price": 799,
        "stock": "Out of Stock",
        "description": "Samsung's flagship Android smartphone.",
        "warranty": "1 year",
    },
    "samsung galaxy a55": {
        "name": "Samsung Galaxy A55",
        "category": "Smartphone",
        "price": 449,
        "stock": "Available",
        "description": "Samsung's mid-range Android smartphone with a large battery.",
        "warranty": "1 year",
    },
    "google pixel 9": {
        "name": "Google Pixel 9",
        "category": "Smartphone",
        "price": 649,
        "stock": "Available",
        "description": "Google's flagship Android phone with an AI-powered camera.",
        "warranty": "1 year",
    },
    "macbook air m3": {
        "name": "MacBook Air M3",
        "category": "Laptop",
        "price": 999,
        "stock": "Available",
        "description": "Lightweight Apple laptop powered by the M3 chip.",
        "warranty": "1 year",
    },
    "macbook pro 14": {
        "name": "MacBook Pro 14",
        "category": "Laptop",
        "price": 1599,
        "stock": "Available",
        "description": "Apple's pro laptop with a 14-inch Liquid Retina XDR display.",
        "warranty": "1 year",
    },
    "dell xps 13": {
        "name": "Dell XPS 13",
        "category": "Laptop",
        "price": 1099,
        "stock": "Available",
        "description": "Compact Windows ultrabook with a InfinityEdge display.",
        "warranty": "1 year",
    },
    "lenovo thinkpad x1 carbon": {
        "name": "Lenovo ThinkPad X1 Carbon",
        "category": "Laptop",
        "price": 1349,
        "stock": "Out of Stock",
        "description": "Business-grade ultralight laptop with a carbon-fiber chassis.",
        "warranty": "2 years",
    },
    "sony wh-1000xm5": {
        "name": "Sony WH-1000XM5",
        "category": "Headphones",
        "price": 399,
        "stock": "Available",
        "description": "Sony's noise-cancelling over-ear headphones.",
        "warranty": "1 year",
    },
    "apple airpods pro": {
        "name": "Apple AirPods Pro",
        "category": "Headphones",
        "price": 249,
        "stock": "Available",
        "description": "Apple's noise-cancelling wireless earbuds.",
        "warranty": "1 year",
    },
    "bose quietcomfort earbuds": {
        "name": "Bose QuietComfort Earbuds",
        "category": "Headphones",
        "price": 279,
        "stock": "Available",
        "description": "Bose's noise-cancelling in-ear earbuds.",
        "warranty": "1 year",
    },
    "ipad air": {
        "name": "iPad Air",
        "category": "Tablet",
        "price": 599,
        "stock": "Available",
        "description": "Apple's mid-range tablet powered by the M2 chip.",
        "warranty": "1 year",
    },
    "samsung galaxy tab s9": {
        "name": "Samsung Galaxy Tab S9",
        "category": "Tablet",
        "price": 799,
        "stock": "Out of Stock",
        "description": "Samsung's flagship Android tablet with an AMOLED display.",
        "warranty": "1 year",
    },
    "apple watch series 9": {
        "name": "Apple Watch Series 9",
        "category": "Smartwatch",
        "price": 399,
        "stock": "Available",
        "description": "Apple's flagship smartwatch with health and fitness tracking.",
        "warranty": "1 year",
    },
    "samsung galaxy watch 6": {
        "name": "Samsung Galaxy Watch 6",
        "category": "Smartwatch",
        "price": 329,
        "stock": "Available",
        "description": "Samsung's Android smartwatch with sleep and fitness tracking.",
        "warranty": "1 year",
    },
    "sony alpha a6400": {
        "name": "Sony Alpha a6400",
        "category": "Camera",
        "price": 899,
        "stock": "Available",
        "description": "Mirrorless APS-C camera with fast autofocus.",
        "warranty": "1 year",
    },
    "gopro hero 12": {
        "name": "GoPro HERO12",
        "category": "Camera",
        "price": 399,
        "stock": "Available",
        "description": "Waterproof action camera with image stabilization.",
        "warranty": "1 year",
    },
    "sony playstation 5": {
        "name": "Sony PlayStation 5",
        "category": "Gaming Console",
        "price": 499,
        "stock": "Out of Stock",
        "description": "Sony's current-generation home gaming console.",
        "warranty": "1 year",
    },
    "nintendo switch oled": {
        "name": "Nintendo Switch OLED",
        "category": "Gaming Console",
        "price": 349,
        "stock": "Available",
        "description": "Nintendo's hybrid handheld/home console with an OLED screen.",
        "warranty": "1 year",
    },
    "lg c3 55-inch oled tv": {
        "name": "LG C3 55-inch OLED TV",
        "category": "Television",
        "price": 1299,
        "stock": "Available",
        "description": "55-inch 4K OLED smart TV with excellent contrast.",
        "warranty": "2 years",
    },
    "amazon echo dot": {
        "name": "Amazon Echo Dot",
        "category": "Smart Speaker",
        "price": 49,
        "stock": "Available",
        "description": "Compact smart speaker with Alexa built in.",
        "warranty": "1 year",
    },
}


def find_product(product_name: str) -> dict | None:
    """
    Looks up a product by name using forgiving, case-insensitive word
    matching against the product's key, full name, AND category - so
    "sony headphones" matches Sony WH-1000XM5 via a shared word with
    each part ("sony" from the name, "headphones" from the category),
    even though the two words aren't contiguous in either field. When
    a query matches multiple products by category alone (e.g. just
    "laptop"), the one with the highest word overlap wins - ties go to
    whichever product comes first in dict order.
    """
    if not product_name:
        return None

    query = product_name.strip().lower()

    # Exact key match first
    if query in PRODUCTS:
        return PRODUCTS[query]

    query_words = set(query.split())

    best_match = None
    best_overlap = 0
    for key, record in PRODUCTS.items():
        searchable_words = set(f"{key} {record['name'].lower()} {record['category'].lower()}".split())
        overlap = len(query_words & searchable_words)
        if overlap > best_overlap:
            best_overlap = overlap
            best_match = record

    return best_match