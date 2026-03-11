# inventory-management-fhnw
Lagerverwaltung (Inventar) für kleine Firmen – FHNW Projekt

Project structure

inventory-system/
│
├─ README.md
├─ requirements.txt
├─ .env.example
├─ .gitignore
│
├─ docs/
│  ├─ screenshots/
│  └─ diagrams/
│
├─ app/
│
│  ├─ main.py
│
│  ├─ models/           # database
│  │  ├─ user.py
│  │  ├─ product.py
│  │  ├─ category.py
│  │  ├─ location.py
│  │  └─ movement.py
│
│  ├─ services/         # backend logic
│  │  ├─ product_service.py
│  │  ├─ inventory_service.py
│  │  └─ user_service.py
│
│  ├─ views/            # frontend
│  │  ├─ dashboard.py
│  │  ├─ product_list.py
│  │  ├─ add_product.py
│  │  └─ movement.py
│
│  └─ seed.py
│
├─ data/
│
└─ tests/
