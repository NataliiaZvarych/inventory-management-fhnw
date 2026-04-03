# 📦 Inventory Management Projekt

> 🚧 add screenshot  ui-image

---

This project was developed as part of the Advanced Programming module at FHNW (BSc Business Information Technology). The goal is to implement a structured backend system using modern Python technologies, clean architecture principles, and ORM-based database management.

---

## 📝 Application Requirements

In small and medium-sized enterprises, inventory management is often performed manually or with inadequate tools. This leads to:
- Inconsistent data
- Lack of transparency in stock levels
- Poor traceability of movements
- A structured system is necessary to store and manage data reliably.

---

### Scenario

The application allows users to:
- manage products, categories, and storage locations
- record inventory movements
- store all data in a relational database
- ensure data consistency and traceability

  ---

## 📖 User Stories

### 1.Manage Products
**As a user, I want to create and manage products.**

- **Inputs:** Product name, category, storage location 
- **Outputs:** Stored product

___

### 2.Manage Categories and Storage Locations
**As a user, I want to define categories and storage locations.**

- **Input:** Category/storage location data
- **Output:** Stored entries

---

### 3.Record Inventory Movements
**As a user, I want to document movements in the inventory.**

- **Input:** Product, quantity, user
- **Output:** Movement record

---

### 4.Manage Users
**As a user, I want to manage users.**

- **Input:** User data
- **Output:** Stored user

---

### 5.Monitor Low Stock
**As a user, I want to receive alerts when stock levels are low so that I can reorder items in time**

- **Inputs:** Product ID, current quantity, minimum stock level.
- **Outputs:** Visual warning or status "Niedriger Bestand" in the UI.

---

### 6.Loan and Return Items
**As a staff member, I want to borrow and return products to track their current usage.**

- **Inputs:** Product, staff member (user), return deadline.
- **Outputs:** Updated movement record and loan status.

---

### 7.Export Data (Admin only)
**As an admin, I want to export product lists and movement data to CSV for external reporting.**

- **Inputs:** Selection of data (Products or Movements), date range. 
- **Outputs:** Generated CSV file.

---

### 8.View Inventory History
**As an admin, I want to see a log of all past movements to track who changed what and when.**

- **Inputs:** Product ID or User ID.
- **Outputs:** List of movements with timestamps and responsible users.

---

### 9. Manage Specific Categories (Sub-types)
**As an admin, I want to define if a category is for sale or for loan to apply different rules.**

- **Inputs:** Category name, type (SaleCategory or LoanCategory), specific attributes like return deadline or min stock level.
- **Outputs:** Specialized category entry.

---

## 🧩 Use Cases

> 🚧 add diagrams for use cases

### Main Use Cases

- Manage Inventory Entities (CRUD)
- Process Goods Transactions (In/Out)
- Manage Loans and Returns
- Audit and Export History (Admin)
- User Authentication and Roles

### Actors

- Staff
- Admin

---

### Wireframes / Mockups


> 🚧 Add screenshots of the wireframe mockups you chose to implement.

---

## 🏛️ Architecture

![UML Class Diagram](app/docs/architecture-diagrams/ClassDiagram.png)



  

