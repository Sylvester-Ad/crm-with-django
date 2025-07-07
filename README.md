# Django CRM App

A full-featured Customer Relationship Management (CRM) web application built with Django and styled using TailwindCSS. This project allows users to manage customer data, track interactions, and perform all CRUD operations in a secure and user-friendly interface.

---

## 🚀 Features

- User authentication (login, logout, password reset via email)
- CRUD functionality for managing customers and records
- Relationship mapping between models with Django ORM
- Dynamic dashboard with filtered data
- Responsive design powered by TailwindCSS
- Email integration for password recovery and user notifications
- Clean, maintainable code with reusable components

---

## 🛠 Tech Stack

- **Backend:** Django
- **Frontend:** TailwindCSS, HTML
- **Database:** SQLite (default), easily switchable to PostgreSQL
- **Email Backend:** Django’s built-in SMTP support
- **Authentication:** Django’s built-in auth system

---

## ⚙️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Sylvester-Ad/crm-with-django.git
cd crm-with-django
```

2. **Create and activate a virtual environment:**

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. **Install the dependencies:**

```bash
pip install -r requirements.txt
```

4. **Apply migrations:**

```bash
python manage.py migrate
```

5. **Create a superuser (admin access):**

```bash
python manage.py createsuperuser
```

6. **Run the development server:**

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

---

## 🔐 Environment Setup

Ensure you set up a `.env` file or add your sensitive variables in `settings.py`, such as:

```env
SECRET_KEY=your_secret_key
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_password
```

*(Optional: You can integrate `python-decouple` or `django-environ` for better env management.)*

---

## 📁 Project Structure

```
├── agents/ # App handling agent logic
├── djcrm/ # Django project configuration
├── leads/ # Core app for lead management
├── static/ # Static files (CSS, JS, images)
├── templates/ # HTML templates
├── db.sqlite3 # SQLite database
├── manage.py # Django project manager
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```

---

## 🙋‍♂️ Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## ✍️ Author

**Sylvester Adade**  
📧 sylvesteradade895@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/sylvester-adade) | [GitHub](https://github.com/Sylvester-Ad)

