## Project Structure

```text
inventory-system/
│
├─ README.md             # Main project documentation
├─ requirements.txt      # Python dependencies
├─ .gitignore            # Git ignore rules
│
├─ app/                  # Main application source code
│  ├─ main.py            # Entry point (starts backend and frontend)
│  │
│  ├─ models/            # Database models
│  │  ├─ user.py         # User model
│  │  ├─ product.py      # Product model
│  │  ├─ category.py     # Category model
│  │  ├─ location.py     # Location model
│  │  └─ movement.py     # StockMovement model
│  │
│  ├─ services/          # Backend business logic
│  │  ├─ product_service.py   # Product operations
│  │  ├─ inventory_service.py # Inventory operations
│  │  └─ user_service.py      # User operations
│  │
│  ├─ views/             # Frontend pages and UI
│  │  ├─ dashboard.py    # Dashboard page
│  │  ├─ product_list.py # Product list page
│  │  ├─ add_product.py  # Add product page
│  │  └─ movement.py     # Inventory movement page
│  │
│  └─ seed.py            # Populate database with initial data
```

Test Commit für Dokumentation Branch
