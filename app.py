import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Custom User-Agent header (required by OpenFoodFacts API documentation)
HEADERS = {"User-Agent": "InventorySystem/1.0 (student@example.com)"}
OPENFOODFACTS_URL = "https://world.openfoodfacts.org/api/v2/product"

# Simulated in-memory inventory database array
inventory = [
    {
        "id": 1,
        "barcode": "737628064502",
        "product_name": "Organic Rice Drink",
        "brands": "RiceSelect",
        "ingredients_text": "Organic Brown Rice, Water, Sea Salt",
        "quantity": 20,
        "price": 3.99
    },
    {
        "id": 2,
        "barcode": "3274080005003",
        "product_name": "Cristaline Water",
        "brands": "Cristaline",
        "ingredients_text": "Spring Water",
        "quantity": 50,
        "price": 0.99
    }
]

# Helper function to query OpenFoodFacts API by barcode
def fetch_from_openfoodfacts(barcode):
    try:
        url = f"{OPENFOODFACTS_URL}/{barcode}.json"
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                product = data.get("product", {})
                return {
                    "product_name": product.get("product_name", "Unknown Product"),
                    "brands": product.get("brands", "Unknown Brand"),
                    "ingredients_text": product.get("ingredients_text", "N/A")
                }
    except requests.RequestException:
        pass
    return None

# --- REST API ROUTES ---

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Inventory Management REST API Running"}), 200

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

@app.route("/inventory", methods=["POST"])
def create_item():
    data = request.get_json() or {}
    barcode = data.get("barcode")

    if not barcode:
        return jsonify({"error": "Barcode is required"}), 400

    # Query OpenFoodFacts API to auto-fill details if available
    external_data = fetch_from_openfoodfacts(barcode)
    
    new_id = max([i["id"] for i in inventory], default=0) + 1
    new_item = {
        "id": new_id,
        "barcode": str(barcode),
        "product_name": data.get("product_name") or (external_data["product_name"] if external_data else "New Item"),
        "brands": data.get("brands") or (external_data["brands"] if external_data else "Generic"),
        "ingredients_text": external_data["ingredients_text"] if external_data else data.get("ingredients_text", "N/A"),
        "quantity": int(data.get("quantity", 0)),
        "price": float(data.get("price", 0.0))
    }
    
    inventory.append(new_item)
    return jsonify(new_item), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json() or {}
    if "quantity" in data:
        item["quantity"] = int(data["quantity"])
    if "price" in data:
        item["price"] = float(data["price"])

    return jsonify(item), 200

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global inventory
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    inventory = [i for i in inventory if i["id"] != item_id]
    return jsonify({"message": f"Item {item_id} deleted successfully"}), 200

@app.route("/external-search/<barcode>", methods=["GET"])
def external_search(barcode):
    details = fetch_from_openfoodfacts(barcode)
    if not details:
        return jsonify({"error": "Product not found on OpenFoodFacts"}), 404
    return jsonify(details), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)