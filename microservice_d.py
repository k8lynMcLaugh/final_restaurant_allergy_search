from flask import Flask, request, jsonify
import math

app = Flask(__name__)

restaurant_locations = {
    "Thai Delight": (45.512230, -122.658722),
    "Green Garden": (45.515450, -122.676207),
    "Pasta Palace": (45.520247, -122.674194)
}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(d_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

@app.route('/search_radius', methods=["GET"])
def search_radius():
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        radius = float(request.args.get('radius'))
    except (TypeError, ValueError):
        return jsonify(error="Missing or invalid lat, lon, or radius"), 400

    nearby = []
    for name, (r_lat, r_lon) in restaurant_locations.items():
        dist = haversine(lat, lon, r_lat, r_lon)
        if dist <= radius:
            nearby.append({"name": name, "distance_km": dist})

    return jsonify(nearby=nearby)

if __name__ == '__main__':
    app.run(port=8084)

