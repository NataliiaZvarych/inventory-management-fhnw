# inventory-management-fhnw
Lagerverwaltung (Inventar) für kleine Firmen – FHNW Projekt

Project structure

## Project Structure

```text
inventory-system/
│
├─ README.md
│  # Main documentation file of the project.
│  # Explains the purpose of the application, technologies used,
│  # project structure, installation instructions, and screenshots.
│
├─ requirements.txt
│  # List of Python dependencies required to run the project.
│  # Example: nicegui, sqlalchemy, python-dotenv, etc.
│  # Install them with: pip install -r requirements.txt
│
├─ .env.example
│  # Example configuration file for environment variables.
│  # It shows which variables are required for the application,
│  # for example DATABASE_URL or SECRET_KEY.
│  # Users copy this file to ".env" and add their own values.
│
├─ .gitignore
│  # Specifies which files Git should ignore.
│  # Typically excludes:
│  # - virtual environments
│  # - database files
│  # - temporary files
│  # - .env files with secrets
│
├─ docs/
│  # Documentation assets used to explain the project.
│  # This folder usually contains screenshots and diagrams.
│
│  ├─ screenshots/
│  │  # Screenshots of the user interface.
│  │  # Used in README or presentations to demonstrate the application.
│  │  # Example:
│  │  # - dashboard.png
│  │  # - product_list.png
│  │  # - add_product.png
│
│  └─ diagrams/
│     # Architecture and design diagrams.
│     # Examples:
│     # - ER diagram (database schema)
│     # - UML diagrams
│     # - system architecture diagrams
│
├─ app/
│  # Main application source code.
│  # Contains the backend logic, frontend UI, and database models.
│
│  ├─ main.py
│  │  # Entry point of the application.
│  │  # Starts the web interface (NiceGUI server) and initializes the app.
│  │  # It connects frontend views with backend services.
│
│  ├─ models/
│  │  # Database models (Data Layer).
│  │  # These files define the database structure using an ORM
│  │  # such as SQLAlchemy.
│  │
│  │  ├─ user.py
│  │  │  # Defines the User model.
│  │  │  # Represents application users such as employees or administrators.
│  │  │  # Typical fields:
│  │  │  # id, name, email, password, role
│  │  │
│  │  ├─ product.py
│  │  │  # Defines the Product model.
│  │  │  # Represents an item stored in the warehouse.
│  │  │  # Typical fields:
│  │  │  # id, name, category_id, location_id, quantity, min_quantity
│  │  │
│  │  ├─ category.py
│  │  │  # Defines the Category model.
│  │  │  # Used to group products into categories such as
│  │  │  # electronics, tools, office supplies, etc.
│  │  │
│  │  ├─ location.py
│  │  │  # Defines the Location model.
│  │  │  # Represents where the product is stored in the warehouse.
│  │  │  # Example: shelf, room, or storage zone.
│  │  │
│  │  └─ movement.py
│  │     # Defines the StockMovement model.
│  │     # Tracks all inventory changes such as:
│  │     # - product added to stock
│  │     # - product removed
│  │     # - product borrowed or returned
│
│  ├─ services/
│  │  # Business logic layer (Backend).
│  │  # Contains functions that implement the main application logic.
│  │  # These services interact with the database models.
│  │
│  │  ├─ product_service.py
│  │  │  # Handles operations related to products.
│  │  │  # Example functions:
│  │  │  # - create_product()
│  │  │  # - update_product()
│  │  │  # - delete_product()
│  │  │  # - get_product_list()
│  │  │
│  │  ├─ inventory_service.py
│  │  │  # Handles inventory operations.
│  │  │  # Example functions:
│  │  │  # - add_stock()
│  │  │  # - remove_stock()
│  │  │  # - borrow_product()
│  │  │  # - return_product()
│  │  │  # - check_low_stock()
│  │  │
│  │  └─ user_service.py
│  │     # Handles user-related logic.
│  │     # Example functions:
│  │     # - create_user()
│  │     # - login_user()
│  │     # - manage roles and permissions
│
│  ├─ views/
│  │  # Frontend layer (User Interface).
│  │  # Contains NiceGUI pages and UI components.
│  │  # These files display data and interact with the backend services.
│  │
│  │  ├─ dashboard.py
│  │  │  # Main dashboard page of the application.
│  │  │  # Displays key information such as:
│  │  │  # - total number of products
│  │  │  # - low stock warnings
│  │  │  # - recent inventory movements
│  │  │
│  │  ├─ product_list.py
│  │  │  # Page that displays all products in a table.
│  │  │  # Allows users to search, filter, and view product details.
│  │  │
│  │  ├─ add_product.py
│  │  │  # Page with a form for adding new products to the system.
│  │  │  # Sends the data to the product_service backend.
│  │  │
│  │  └─ movement.py
│  │     # Page used to record inventory movements.
│  │     # Example:
│  │     # - borrowing equipment
│  │     # - returning items
│  │     # - updating stock levels
│
│  └─ seed.py
│     # Script used to populate the database with initial test data.
│     # Example:
│     # - sample users
│     # - sample products
│     # - example categories
│     # This helps demonstrate the application during development.
│
├─ data/
│  # Directory where the SQLite database file is stored.
│  # Example:
│  # inventory.db
│  # Usually ignored by Git because it contains runtime data.
│
└─ tests/
   # Automated tests for the application.
   # Used to verify that the business logic works correctly.
   # Example tests:
   # - product creation
   # - inventory updates
   # - stock validation
```

