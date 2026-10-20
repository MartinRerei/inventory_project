import sys
import requests

API_BASE = "http://127.0.0.1:5000"

def print_menu():
    print("\n==========================================")
    print("      INVENTORY MANAGEMENT SYSTEM         ")
    print("==========================================")
    print("1. View All Inventory Items")
    print("2. Search OpenFoodFacts API by Barcode")
    print("3. Add New Item (Fetch from External API)")
    print("4. Update Item Price / Stock Level")
    print("5. Delete Item from Inventory")
    print("6. Exit")
    print("==========================================")

def view_inventory():
    try:
        res = requests.get(f"{API_BASE}/inventory")
        if res.status_code == 200:
            items = res.json()
            print(f"\n--- INVENTORY LIST ({len(items)} items) ---")
            for item in items:
                print(f"ID: {item['id']} | Barcode: {item['barcode']} | Name: {item['product_name']} | Brand: {item['brands']} | Stock: {item['quantity']} | Price: ${item['price']:.2f}")
        else:
            print("[Error] Failed to fetch inventory.")
    except requests.ConnectionError:
        print("[Error] Could not connect to API server. Run 'python app.py' in another terminal tab!")

def search_external():
    barcode = input("Enter barcode to lookup on OpenFoodFacts: ").strip()
    try:
        res = requests.get(f"{API_BASE}/external-search/{barcode}")
        if res.status_code == 200:
            data = res.json()
            print("\n--- EXTERNAL PRODUCT DATA ---")
            print(f"Product Name: {data['product_name']}")
            print(f"Brands:       {data['brands']}")
            print(f"Ingredients:  {data['ingredients_text']}")
        else:
            print(f"[404] Product barcode '{barcode}' not found on OpenFoodFacts.")
    except requests.ConnectionError:
        print("[Error] API server offline.")

def add_item():
    barcode = input("Enter barcode: ").strip()
    quantity = input("Enter initial stock quantity: ").strip()
    price = input("Enter unit price: ").strip()

    payload = {
        "barcode": barcode,
        "quantity": int(quantity) if quantity.isdigit() else 0,
        "price": float(price) if price.replace('.', '', 1).isdigit() else 0.0
    }

    try:
        res = requests.post(f"{API_BASE}/inventory", json=payload)
        if res.status_code == 201:
            item = res.json()
            print(f"\n[Success] Item added! ID: {item['id']} - Name: '{item['product_name']}'")
        else:
            print(f"[Error] {res.json().get('error', 'Failed to add item')}")
    except requests.ConnectionError:
        print("[Error] API server offline.")

def update_item():
    item_id = input("Enter Item ID to update: ").strip()
    quantity = input("Enter new quantity (leave blank to skip): ").strip()
    price = input("Enter new price (leave blank to skip): ").strip()

    payload = {}
    if quantity.isdigit():
        payload["quantity"] = int(quantity)
    if price.replace('.', '', 1).isdigit():
        payload["price"] = float(price)

    if not payload:
        print("[Cancel] No fields provided to update.")
        return

    try:
        res = requests.patch(f"{API_BASE}/inventory/{item_id}", json=payload)
        if res.status_code == 200:
            print(f"[Success] Item {item_id} updated successfully!")
        else:
            print(f"[Error] {res.json().get('error', 'Update failed')}")
    except requests.ConnectionError:
        print("[Error] API server offline.")

def delete_item():
    item_id = input("Enter Item ID to delete: ").strip()
    try:
        res = requests.delete(f"{API_BASE}/inventory/{item_id}")
        if res.status_code == 200:
            print(f"[Success] Item {item_id} removed.")
        else:
            print(f"[Error] {res.json().get('error', 'Delete failed')}")
    except requests.ConnectionError:
        print("[Error] API server offline.")

def main():
    while True:
        print_menu()
        choice = input("Select an option (1-6): ").strip()
        if choice == "1":
            view_inventory()
        elif choice == "2":
            search_external()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            print("Exiting CLI Admin Portal. Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()