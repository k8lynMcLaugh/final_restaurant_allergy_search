import requests
import sys

MICROSERVICE_A = "http://localhost:8081"
MICROSERVICE_B = "http://localhost:8082"
MICROSERVICE_C = "http://localhost:8083"
MICROSERVICE_D = "http://localhost:8084"

user = None  # Will store {'username': str, 'email': str}

def register():
    print("\n== Register ==")
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password (6+ chars): ").strip()

    resp = requests.post(f"{MICROSERVICE_A}/register", json={
        "username": username,
        "email": email,
        "password": password
    })

    data = resp.json()
    print(data.get("message", "No message received."))

def login():
    global user
    print("\n== Login ==")
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    resp = requests.post(f"{MICROSERVICE_A}/login", json={
        "email": email,
        "password": password
    })

    data = resp.json()
    print(data.get("message", "No message received."))

    if data.get("success"):
        user = {"username": data.get("username"), "email": email}

def view_favorites():
    if not user:
        print("Please login first.")
        return

    resp = requests.get(f"{MICROSERVICE_A}/favorites/{user['username']}")
    data = resp.json()
    favs = data.get("favorites", [])
    print(f"\nYour favorite restaurants: {', '.join(favs) if favs else 'None'}")

def search_restaurants():
    if not user:
        print("Please login first.")
        return

    print("\n== Search Nearby Restaurants ==")
    try:
        lat = float(input("Your latitude (e.g. 45.512): ").strip())
        lon = float(input("Your longitude (e.g. -122.658): ").strip())
        radius = float(input("Search radius in km (e.g. 5): ").strip())
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return

    resp = requests.get(f"{MICROSERVICE_D}/search_radius", params={
        "lat": lat,
        "lon": lon,
        "radius": radius
    })

    data = resp.json()
    nearby = data.get("nearby", [])

    if not nearby:
        print("No restaurants found nearby.")
        return

    print("\nRestaurants found:")
    for i, r in enumerate(nearby):
        print(f"{i+1}. {r['name']} ({r['distance_km']:.2f} km)")

    try:
        choice = int(input("Choose a restaurant number to view details (0 to cancel): ").strip())
        if choice == 0:
            return
        restaurant = nearby[choice - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    restaurant_name = restaurant['name']
    exclude_allergens = input("Enter allergens to exclude (comma separated), or leave blank: ").strip()

    # Get safe menu
    resp = requests.get(f"{MICROSERVICE_B}/safe_menu", params={
        "restaurant": restaurant_name,
        "exclude_allergens": exclude_allergens
    })
    safe_menu = resp.json().get("safe_menu", [])

    # Get hours/status
    resp = requests.get(f"{MICROSERVICE_C}/hours_status", params={"restaurant": restaurant_name})
    hours_status = resp.json()

    # Check if favorite
    is_favorite = False
    resp = requests.get(f"{MICROSERVICE_A}/favorites/{user['username']}")
    favs = resp.json().get("favorites", [])
    if restaurant_name in favs:
        is_favorite = True

    print(f"\n--- Details for {restaurant_name} ---")
    print(f"Safe menu items (excluding: {exclude_allergens}): {', '.join(safe_menu) if safe_menu else 'None'}")
    print(f"Open hours: {hours_status.get('open_hour')} - {hours_status.get('close_hour')}")
    print(f"Currently open: {'Yes' if hours_status.get('is_open') else 'No'}")
    print(f"In your favorites: {'Yes' if is_favorite else 'No'}")

def main_menu():
    print("\n==== Restaurant Allergy Search ====")
    print("1. Register")
    print("2. Login")
    print("3. View My Favorite Restaurants")
    print("4. Search Nearby Restaurants")
    print("5. Exit")

    choice = input("Select an option: ").strip()
    return choice

def main():
    print("Welcome to the Restaurant Allergy Search App!")
    while True:
        choice = main_menu()
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            view_favorites()
        elif choice == "4":
            search_restaurants()
        elif choice == "5":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()

