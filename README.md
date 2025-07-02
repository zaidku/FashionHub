# 👕 FashionHub Inventory Management System 🛍️

A modern inventory and ERP system designed for fashion retailers and small businesses. Built with Django, TailwindCSS, and Chart.js — FashionHub gives you powerful tools in a sleek interface to manage your stock, track sales, and grow your brand.

---

## 🚀 Features

- 🔐 Admin Login / Authentication System
- 🧾 Add, Edit, and Delete Products via Modal
- 📦 Inventory Dashboard with Reorder Alerts
- 📊 Visual Sales & Category Charts (Chart.js)
- 🔍 Filter by Category, Size, Color, Status
- 📁 Image Upload Support for Products
- 📤 Export Options for Product Listings
- 🧠 Clean Codebase, Easy to Customize

---
Main Dashboard View
![image](https://github.com/user-attachments/assets/16402e98-d0bc-4e08-9b3d-de787400cc1e)

Inventory View
![image](https://github.com/user-attachments/assets/5bcbcd94-4c02-4eab-b5e7-eca4125f262c)

Add Product
![image](https://github.com/user-attachments/assets/b2a59c90-7626-4639-a1b1-6de640c54322)


Sales View which you can Add Product from and export reports 
![image](https://github.com/user-attachments/assets/a1847f30-ff4a-4418-a21e-c169f76c5307)

New Sale
![image](https://github.com/user-attachments/assets/16c3eb35-13c4-4b0e-88a4-dcc5b759c1ed)

Accounting View
![image](https://github.com/user-attachments/assets/8a515d32-5c1d-44ea-8851-97adb8667486)
![image](https://github.com/user-attachments/assets/cf24d575-1bb1-406f-9a4d-d08585d28b49)

Settings View
![image](https://github.com/user-attachments/assets/3ab3b6ac-34c1-4456-9a6a-9201e5103662)
![image](https://github.com/user-attachments/assets/f75ec89e-951d-4030-a104-1ad970efe4cc)



- 📸 Dashboard with sales, charts, and stats
- 🧾 Add Product modal form
- 🧺 Product Table with live stock info

---

## ⚙️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** Tailwind CSS, HTML5, JavaScript
- **Charts:** Chart.js
- **Database:** SQLite (default, swappable)
- **UI:** Responsive, dark/light-ready, sleek ✨

---

## 📦 Installation

```bash
# 1. Clone the repo
git clone https://github.com/zaidku/FashionHub.git
cd FashionHub

# 2. Create virtual environment
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run the server
python manage.py runserver


🔑 Demo Login
Username: admin
Password: admin123


📁 Project Structure
FashionHub/
├── app/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
├── FashionHub/
│   ├── settings.py
│   ├── urls.py
├── manage.py
├── requirements.txt
└── README.md


🧠 Ideas for Next Version
 PDF export for invoices

 Low stock SMS alerts

 Multi-user support (admin/staff roles)

 REST API for mobile apps

 Barcode scanner support



📄 License
MIT — Free to use, modify, and distribute.
Crafted with ❤️ by @zaidku
