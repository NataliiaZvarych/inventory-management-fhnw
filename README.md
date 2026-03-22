# 📦 Inventory Management System

A simple and efficient **inventory management system** developed in **Python**, designed to manage products, categories, locations, and stock movements.

This project uses **SQLAlchemy** and **SQLite** to provide a structured and reliable database layer, with full traceability of inventory operations.

---

## 🚀 Features

* Product management
* Category and location organization
* User-based stock operations
* Stock movement tracking (add, remove, borrow, return)
* Automatic low-stock detection
* CSV export of product data
* Clean modular architecture (models, services, views)

---

## 🛠️ Technologies

* Python
* SQLAlchemy
* SQLite
* CSV

---

## 📁 Project Structure

```bash
inventory-system/
│
├── README.md              # Main project documentation
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore rules
│
├── app/                   # Main application
│   ├── main.py            # Entry point (starts backend and frontend)
│
│   ├── models/            # Database models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── location.py
│   │   └── movement.py
│
│   ├── services/          # Business logic
│   │   ├── product_service.py
│   │   ├── inventory_service.py
│   │   └── user_service.py
│
│   ├── views/             # UI / frontend
│   │   ├── dashboard.py
│   │   ├── product_list.py
│   │   ├── add_product.py
│   │   └── movement.py
│
│   └── seed.py            # Populate database with initial data
```

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/inventory-system.git
cd inventory-system
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the application:

```bash
python app/main.py
```

Populate the database with initial data:

```bash
python app/seed.py
```

---

## 🗄️ Database Implementation

The database layer of the system was designed and implemented using **SQLAlchemy** and **SQLite**.

### 📦 Entities

* User
* Product
* Category
* Location
* StockMovement

---

### 🔗 Relationships

* Product → Category
* Product → Location
* StockMovement → Product
* StockMovement → User

---

### ⚙️ Data Model Features

Each product includes:

* `quantity` → current stock
* `min_quantity` → threshold for warnings
* `status` → (`available` or `low_stock`)

The system automatically updates product status based on stock levels.

---

### 🔄 Stock Movement Tracking

All inventory changes are recorded in the database:

* `add`
* `remove`
* `borrow`
* `return`

Each movement contains:

* `product_id`
* `user_id`
* `quantity`
* `timestamp`

This ensures **full traceability** of stock changes.

---

### 📁 CSV Export

Database data can be exported to:

`products.csv`

The file contains:

* `product_id`
* `name`
* `quantity`
* `status`

---

## 👨‍💻 Author & Contribution

### Database Development (My Work)

* Designed and implemented the database schema
* Created all database models:

  * Product
  * Category
  * Location
  * User
  * StockMovement
* Defined relationships between entities
* Implemented stock-related fields:

  * `quantity`
  * `min_quantity`
  * `status`
* Ensured data consistency and movement tracking
* Developed CSV export functionality

---

## 📌 Future Improvements

* REST API integration
* Authentication system
* Advanced reporting and analytics
* Web-based UI improvements

---

## 📄 License

This project is for educational purposes.
