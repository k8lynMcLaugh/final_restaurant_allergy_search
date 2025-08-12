from flask import Flask, request, jsonify

app = Flask(__name__)

restaurant_menus = {
    "Thai Delight": {
        "Pad Thai": ["peanuts"],
        "Green Curry": ["milk"],
        "Spring Rolls": []
    },
    "Green Garden": {
        "Salad": [],
        "Peanut Soup": ["peanuts"],
        "Veggie Stir Fry": []
    },
    "Pasta Palace": {
        "Spaghetti": [],
        "Alfredo Sauce": ["milk"],
        "Garlic Bread": ["gluten"]
    }
}

@app.route('/safe_menu', methods=["GET"])
def safe_menu():
    restaurant = request.args.get('restaurant')
    exclude_allergens = request.args.get('exclude_allergens', '')
    exclude_list = [a.strip() for a in exclude_allergens.split(',') if a.strip()]

    if restaurant not in restaurant_menus:
        return jsonify({"error": "Restaurant not found"}), 404

    safe_items = []
    for item, allergens in restaurant_menus[restaurant].items():
        if not any(a in exclude_list for a in allergens):
            safe_items.append(item)

    return jsonify(safe_menu=safe_items)

if __name__ == '__main__':
    app.run(port=8082)

