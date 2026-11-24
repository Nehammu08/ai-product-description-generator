# Product Description Generator - Task AI-CM-008
# Neha Samudrala (DAS014399)
# Idea: take product details -> make short desc, bullets, long desc, SEO meta for each platform.
# I am using templates + some basic NLP (stopword removal, word count) because no database is needed.

import json
import random
import re
from collections import Counter

# words that don't help in keywords
STOP_WORDS = ["the", "a", "an", "and", "is", "are", "it", "this", "very", "but", "of", "to", "for", "with", "i", "my"]

# each platform has its own limits and tone
PLATFORMS = {
    "amazon":       {"short_max": 500, "long_max": 2000, "bullets": 5, "tone": "professional"},
    "flipkart":     {"short_max": 400, "long_max": 1500, "bullets": 4, "tone": "friendly"},
    "shopify":      {"short_max": 300, "long_max": 1200, "bullets": 4, "tone": "premium"},
    "woocommerce":  {"short_max": 400, "long_max": 1500, "bullets": 5, "tone": "professional"},
    "social_media": {"short_max": 150, "long_max": 500,  "bullets": 3, "tone": "casual"},
}

# different words + call to action for each tone
TONES = {
    "professional": {"adj": ["reliable", "high-quality", "dependable"],
                     "cta": "Order the {name} today and feel the difference."},
    "friendly":     {"adj": ["handy", "smart", "useful"],
                     "cta": "Grab your {name} today, you will love it!"},
    "premium":      {"adj": ["refined", "exceptional", "elegant"],
                     "cta": "Discover the {name}, made for people who expect more."},
    "casual":       {"adj": ["awesome", "cool", "must-have"],
                     "cta": "Tap to get the {name} now!"},
    "youthful":     {"adj": ["trendy", "stylish", "fresh"],
                     "cta": "Get your {name} now and stand out!"},
}

# feature word -> what the customer gets (benefit). Easy to add more.
BENEFITS = {
    "battery": "stay powered for days without charging",
    "heart rate": "keep track of your health all day",
    "gps": "track your routes accurately",
    "water": "use it in rain or workouts without worry",
    "display": "see everything clearly, even in sunlight",
    "wireless": "move freely without wires",
    "noise": "focus without distractions",
    "camera": "capture clear photos and videos",
    "fast charging": "get back to full power in minutes",
    "lightweight": "wear it all day without feeling tired",
}

GOOD_WORDS = ["good", "great", "love", "excellent", "amazing", "accurate", "comfortable", "bright", "best"]
BAD_WORDS = ["bad", "slow", "poor", "cheap", "broke", "worst", "uncomfortable"]


def parse_product(data):
    """check the product data and fill missing things"""
    if "name" not in data:
        raise ValueError("product needs a name")
    product = dict(data)
    if isinstance(product.get("features"), str):          # "a, b, c" -> list
        product["features"] = [f.strip() for f in product["features"].split(",")]
    product.setdefault("features", [])
    product.setdefault("category", "product")
    product.setdefault("target_audience", "everyone")
    product.setdefault("main_benefit", "better results")
    product.setdefault("reviews", [])
    return product


def get_benefit(feature):
    """find the benefit for a feature, else a general one"""
    for word in BENEFITS:
        if word in feature.lower():
            return BENEFITS[word]
    return "get dependable performance"


def get_keywords(product):
    """keywords from category + features + most common review words"""
    keywords = [product["category"].lower()]
    for f in product["features"]:
        keywords.append(f.lower())
    for modifier in ["best", "buy", "affordable"]:
        keywords.append(modifier + " " + product["category"].lower())
    # frequent words from reviews
    words = re.findall(r"[a-z]+", " ".join(product["reviews"]).lower())
    words = [w for w in words if w not in STOP_WORDS and len(w) > 3]
    for word, count in Counter(words).most_common(3):
        keywords.append(word)
    return list(dict.fromkeys(keywords))      # remove duplicates, keep order


def analyse_reviews(reviews):
    """very basic sentiment: count good words vs bad words"""
    good, bad = Counter(), Counter()
    for review in reviews:
        for word in re.findall(r"[a-z]+", review.lower()):
            if word in GOOD_WORDS:
                good[word] += 1
            if word in BAD_WORDS:
                bad[word] += 1
    score = sum(good.values()) - sum(bad.values())
    mood = "positive" if score > 0 else "negative" if score < 0 else "mixed"
    return {"sentiment": mood,
            "praised": [w for w, c in good.most_common(3)],
            "complaints": [w for w, c in bad.most_common(3)]}


def cut_text(text, limit):
    """cut at a space so a word is not broken in the middle"""
    if len(text) <= limit:
        return text
    return text[:limit - 3].rsplit(" ", 1)[0] + "..."


def short_description(product, platform, tone):
    adj = random.choice(TONES[tone]["adj"])
    article = "an" if adj[0] in "aeiou" else "a"      # a / an fix
    text = f"Meet the {product['name']}, {article} {adj} {product['category'].lower()} made for {product['target_audience']}."
    if product["features"]:
        text += " Features: " + ", ".join(product["features"][:3]) + "."
    return cut_text(text, PLATFORMS[platform]["short_max"])


def bullet_points(product, platform, review_info):
    count = PLATFORMS[platform]["bullets"]
    bullets = []
    for feature in product["features"][:count]:
        bullets.append(feature.upper() + ": " + get_benefit(feature).capitalize() + ".")
    # review based bullet
    if review_info["praised"] and len(bullets) < count:
        bullets.append("CUSTOMER FAVOURITE: Buyers call it " + ", ".join(review_info["praised"]) + ".")
    return bullets


def long_description(product, platform, tone, review_info):
    parts = [f"The {product['name']} helps you {product['main_benefit']}."]
    for feature in product["features"][:4]:
        parts.append(f"With {feature}, you can {get_benefit(feature)}.")
    if review_info["sentiment"] == "positive":
        parts.append("Customer reviews are mostly positive.")
    parts.append(TONES[tone]["cta"].format(name=product["name"]))
    return cut_text(" ".join(parts), PLATFORMS[platform]["long_max"])


def seo_meta(product):
    title = f"{product['name']} | {product['category']}"
    meta = f"Buy {product['name']} online. Best {product['category'].lower()} for {product['target_audience']}."
    return {"title": cut_text(title, 60), "meta_description": cut_text(meta, 160)}


def generate(data, platform="amazon", tone=None):
    """main function - makes everything for one platform"""
    if platform not in PLATFORMS:
        platform = "amazon"
    product = parse_product(data)
    tone = tone or PLATFORMS[platform]["tone"]
    reviews = analyse_reviews(product["reviews"])
    return {
        "platform": platform,
        "tone": tone,
        "short_description": short_description(product, platform, tone),
        "bullet_points": bullet_points(product, platform, reviews),
        "long_description": long_description(product, platform, tone, reviews),
        "seo": seo_meta(product),
        "keywords": get_keywords(product),
        "review_insights": reviews,
    }


def ab_variants(data, platform="amazon", count=3):
    """same product, different tones -> compare which one is better"""
    tones = list(TONES.keys())
    return [{"variant": "ABC"[i], **{k: v for k, v in generate(data, platform, tones[i]).items()
             if k in ("tone", "short_description")}} for i in range(count)]


if __name__ == "__main__":
    random.seed(1)
    product = {
        "name": "SmartWatch Pro X",
        "category": "Smartwatch",
        "features": "Heart Rate Monitor, GPS Tracking, Water Resistant, 7-Day Battery, AMOLED Display",
        "target_audience": "fitness enthusiasts",
        "main_benefit": "track your health and fitness goals",
        "reviews": ["Great battery life and bright display", "Accurate heart rate, love it",
                    "GPS is slow but overall good", "Strap feels cheap"],
    }
    result = generate(product, "amazon")
    print(json.dumps(result, indent=2))
    print("\n--- A/B variants (flipkart) ---")
    for v in ab_variants(product, "flipkart"):
        print(v["variant"], v["tone"], "->", v["short_description"])
    print("\n--- new tone: youthful (shopify) ---")
    print(generate(product, "shopify", "youthful")["short_description"])
    print("\n--- all platforms ---")
    for p in PLATFORMS:
        r = generate(product, p)
        print(p, "| short:", len(r["short_description"]), "| bullets:", len(r["bullet_points"]))
    with open("output_descriptions.json", "w") as f:
        json.dump(result, f, indent=2)
