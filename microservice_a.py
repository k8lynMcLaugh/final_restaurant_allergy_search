from flask import Flask, request, jsonify

app = Flask(__name__)

USERS_FILE = "users.txt"

def validate_fields(username, email, password):
    if not username or not email or not password:
        return False, "All fields are required"
    if "@" not in email:
        return False, "Invalid email format"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, ""

def check_user_exists(username, email):
    try:
        with open(USERS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) < 3:
                    continue
                if parts[0] == username or parts[1] == email:
                    return True
    except FileNotFoundError:
        return False
    return False

def save_user(username, email, password):
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{email},{password}\n")

def authenticate(email, password):
    try:
        with open(USERS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) < 3:
                    continue
                if parts[1] == email and parts[2] == password:
                    return True, parts[0]
    except FileNotFoundError:
        return False, None
    return False, None

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username", "")
    email = data.get("email", "")
    password = data.get("password", "")

    valid, msg = validate_fields(username, email, password)
    if not valid:
        return jsonify(success=False, message=msg)

    if check_user_exists(username, email):
        return jsonify(success=False, message="Username or email already exists")

    save_user(username, email, password)
    return jsonify(success=True, message=f"User {username} registered successfully")

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email", "")
    password = data.get("password", "")

    if not email or not password:
        return jsonify(success=False, message="Email and password required")

    success, username = authenticate(email, password)
    if success:
        return jsonify(success=True, message=f"Welcome back, {username}!", username=username)
    else:
        return jsonify(success=False, message="Invalid email or password")

@app.route("/favorites/<username>", methods=["GET"])
def get_favorites(username):
    # Hardcoded favorites for demo purposes
    favorites_map = {
        "alice": ["Thai Delight", "Green Garden"],
        "bob": ["Pasta Palace"]
    }
    favs = favorites_map.get(username.lower(), [])
    return jsonify(favorites=favs)

if __name__ == "__main__":
    app.run(port=8081)

