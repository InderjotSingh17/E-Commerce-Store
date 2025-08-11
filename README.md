# 🛒 E-Commerce Store

A fully functional and modern E-Commerce Store built with **Django**, **Stripe**, and **Bootstrap**. This web application supports product listing, cart management, order placement, and secure Stripe-based checkout — all styled with a clean responsive UI.

---

## 🚀 Features

- 🔐 User Signup, Login & Authentication
- 📦 Product Catalog with Pagination
- 🛒 Add to Cart / Quantity Management
- 📋 Order Summary with Total Price
- 💳 Stripe Checkout Integration (Test Mode)
- 📁 Django Admin Panel for Products, Orders
- 📷 Product Image Upload (Media Support)
- 🎨 Fully Responsive UI using Bootstrap 5 & crispy-forms

---

## 🧰 Tech Stack

| Layer       | Technology                            |
|-------------|----------------------------------------|
| Backend     | Django 5.2.4, Python 3.12              |
| Frontend    | Bootstrap 5, HTML5, crispy-forms       |
| Database    | SQLite (development) / MySQL (optional)|
| Payments    | Stripe API (Test Mode)                 |
| Auth        | Django Authentication System           |
| Dev Tools   | Git, GitHub, VS Code, Python-dotenv    |

---

## 🏁 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/InderjotSingh17/E-Commerce-Store.git
cd E-Commerce-Store

2️⃣ Create Virtual Environment

python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Setup Environment Variables

Create a .env file in the root directory:

SECRET_KEY=your_secret_key
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key

5️⃣ Run Migrations

python manage.py migrate

6️⃣ Start Server

python manage.py runserver
Visit: http://127.0.0.1:8000

🤝 Contributing

We welcome contributions from everyone! 💡
Please read our CONTRIBUTING.md and CODE_OF_CONDUCT.md before starting.
Check our open issues — beginner-friendly ones are labeled good first issue.
You can contribute to code, UI/UX improvements, documentation, or testing.

📜 License

This project is licensed under the MIT License.

💬 Contact

Author: Inderjot Singh
📧 Email: singhinderjot816@gmail.com
🌐 GitHub Profile

⭐ Support

If you like this project, consider giving it a ⭐ on GitHub to support development!


