from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

restaurant_hours = {
    "Thai Delight": {"open": 11, "close": 21},
    "Green Garden": {"open": 10, "close": 20},
    "Pasta Palace": {"open": 12, "close": 22}
}

@app.route('/hours_status', methods=["GET"])
def hours_status():
    restaurant = request.args.get('restaurant')
    if restaurant not in restaurant_hours:
        return jsonify({"error": "Restaurant not found"}), 404

    now_hour = datetime.now().hour
    hours = restaurant_hours[restaurant]
    is_open = hours["open"] <= now_hour < hours["close"]

    return jsonify(open_hour=hours["open"], close_hour=hours["close"], is_open=is_open)

if __name__ == '__main__':
    app.run(port=8083)

