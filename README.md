# Sulfur Electric Tattoo
### VIDEO DEMO: 
---
# DESCRIPTION
Sulfur Electric Tattoo is a full-stack web application, that allows users to browse through gallery of a tattoo artist, who kindly allowed me to use his work and face to create building blocks for the app. Beyond browsing, the user can book an appointment by registering his details on a simple "Book a consultation" form.
Furthermore, for the administrator's assistance the app has a password-protected admin panel to view, approve, or delete bookings and upload new portfolio images.
The project combines everything I learned in CS50 Introduction to Computer Science 2025: Flask and Jinja2 for backend and templates, SQLite with Flask-SQLAlchemy, HTML, CSS/Bootstrap and JavaScript for a front-end.
I have chosen to make this app, because the tattoo artist, a friend of mine, was in need of acquiring new clients and I offered to make a web application for him.
This project represents exactly how I visualize a tattoo studio website - fast, minimalistic, with simple booking form and user-friendly interface.

---

# SCREENSHOTS

| <img src="for_readme/SULFUR ELECTRIC TATTOO 1.jpg" alt="Tattoo 1" width="220" /> | <img src="for_readme/SULFUR ELECTRIC TATOO.jpg" alt="Portfolio sample" width="220" /> | <img src="for_readme/SULFUR ELECTRIC TATTOO 2.jpg" alt="Tattoo 2" width="220" /> |
|---|---|---|


| <img src="for_readme/SULFUR ELECTRIC TATTOO 3.jpg" alt="Tattoo 3" width="220" /> | <img src="for_readme/SULFUR ELECTRIC TATTOO 4.jpg" alt="Tattoo 4" width="220" /> | <img src="for_readme/SULFUR ELECTRIC TATTOO 5 ADMIN PANEL.jpg" alt="Tattoo 5 (admin)" width="220" /> |
|---|---|---|


| <img src="for_readme/SULFUR ELECTRIC TATOO 6 admin panel.jpg" alt="Sulfur Electric Tattoo 6" width="220" /> | <img src="for_readme/SULFUR ELECTRIC TATOO admin.jpg" alt="Admin panel" width="220" /> | <img src="for_readme/SULFUR ELECTRIC TATTOO ADMIN PANEL 7.jpg" alt="Admin panel 7" width="220" /> |
|---|---|---|

# QUICK START

Prerequisites
- Git (to clone the repo)
- Python 3.8+

Clone the repository:

```bash
git clone https://github.com/artrosaurus/Final-Project-cs50.git
cd Final-Project-cs50
```

Create a virtual environment and install requirements

Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Windows (PowerShell)
```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a local `.env` (do NOT commit this for security reasons)

```text
SECRET_KEY=<generate-a-secret-key>
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=<paste-generated-password-hash-here>
```

Generate values (inside the activated venv)

Generate a SECRET_KEY (secure random):
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Generate an admin password hash (replace `your-password`):
```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your-password'))"
```

Run the app (inside the activated virtualenv)

Linux / macOS
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
# or just:
python app.py
```

Windows (PowerShell)
```powershell
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run
# or just:
python app.py
```

Open http://127.0.0.1:5000 in your browser. The first time you run the app it will create `tattoo.db`.

Populate the gallery:
- Use the admin panel (login at `/login-admin`) and upload images via the admin panel. This stores files in `static/images` and creates DB records.

Populate bookings:
- Users can create bookings by filling the "Book a consultation" form on the site (`/booking`). Submitting the form will add a booking to the database.

---
# FILES
---

- `app.py` — Flask application and routes
- `requirements.txt` — Python dependencies
- `.gitignore` — files ignored by Git
- `templates/` — Jinja2 HTML templates
	- `templates/index.html` — home / hero
	- `templates/portfolio.html` — gallery page and overlay
	- `templates/admin.html` — admin dashboard
	- `templates/login-admin.html` — admin login page
	- `templates/booking.html` — booking form
	- `templates/contact.html` — contact page
	- `templates/layout.html` — base layout (nav/footer)
- `static/` — static assets
	- `static/css/style.css` — main stylesheet
	- `static/js/main.js` — small frontend scripts (gallery overlay)
	- `static/images/` — shipped images used by the site
		- (several photos and placeholders)

---
# DESIGN CHOICES 

---

