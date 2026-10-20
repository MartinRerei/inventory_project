# Inventory Management REST API & CLI Portal

A full-stack Python application built with Flask and integrated with the external [OpenFoodFacts API](https://world.openfoodfacts.org). The system provides an administrator portal for managing retail inventory through CRUD operations and a command-line interface (CLI).

---

## Features

- **RESTful Flask API**: Complete CRUD operations (`GET`, `POST`, `PATCH`, `DELETE`) with standard HTTP status codes.
- **External API Integration**: Automatically fetches and enriches product details (product name, brand, ingredients) from OpenFoodFacts using product barcodes.
- **Interactive CLI Admin Portal**: Terminal-based interface for employees to view, add, update, search, and delete inventory items.
- **Automated Testing Suite**: Full `pytest` test suite with `unittest.mock` to validate endpoints and external API calls offline.
- **Custom User-Agent Compliance**: Uses compliant User-Agent headers required by OpenFoodFacts API policies.

---

## File Structure

```text
inventory_project/
├── app.py          # Flask REST API server & OpenFoodFacts integration
├── cli.py          # Terminal CLI application for managing inventory
├── test_app.py     # Automated unit tests using pytest and unittest.mock
└── README.md       # Project documentation and usage guide