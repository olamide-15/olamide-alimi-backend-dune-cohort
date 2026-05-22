# Toriloshop — Production Setup Documentation

## Project Description

Toriloshop is a Django-based e-commerce application that was configured and deployed for production. The changes made focused on hardening the app for a live environment: securing secrets via environment variables, serving static files efficiently, connecting to a production-grade database, and running the app with a production WSGI server.


## Production Changes Made

The following updates were applied to prepare toriloshop for production:

### 1. `.env` File — Secret & Config Management

Sensitive settings were moved out of `settings.py` and into a `.env` file, which is never committed to version control.

**Variables stored in `.env`:**

SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=sqlite:///db.sqlite3

### 2. Gunicorn — Production WSGI Server

Django's built-in development server (`manage.py runserver`) is **not suitable for production**. Gunicorn was added as the production WSGI server.

**Installation:**

```bash
pip install gunicorn
```

**Running the app:**

```bash
gunicorn toriloshop.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

| Flag | Purpose |
|------|---------|
| `--bind 0.0.0.0:8000` | Listens on all interfaces, port 8000 |
| `--workers 3` | Spawns 3 worker processes (recommended: 2 × CPU cores + 1) |

Gunicorn is typically placed behind a reverse proxy like **Nginx**.

a watress was installed altarnatively

### 3. WhiteNoise — Static File Serving

In production, Django does not serve static files by default. **WhiteNoise** was added to serve them directly from the application, without needing a separate web server or CDN for static assets.

**Installation:**

```bash
pip install whitenoise
```

**Configuration in `settings.py`:**

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ← Add right after SecurityMiddleware
    ...
]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Optional: enable compression and long-term caching
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

**Collect static files before deployment:**

```bash
python manage.py collectstatic
```

---

### 4. `dj-database-url` — Database Configuration

Instead of hardcoding database credentials, `dj-database-url` was used to parse a `DATABASE_URL` connection string from the environment.

**Installation:**

```bash
pip install dj-database-url psycopg2-binary
```

**Configuration in `settings.py`:**

```python
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
    )
}
```

This makes it straightforward to swap databases (SQLite locally, PostgreSQL in production) with a single environment variable.

---

## Setup Instructions


### Step 1 — Clone the Repository
git clone https://github.com/your-username/toriloshop.git


---

### Step 2 — Create a Virtual Environment & Install Dependencies
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


### Step 3 — Set Up the `.env` File
Copy the example environment file and fill in your values:
 .env.example .env


Open `.env` and configure:


SECRET_KEY=replace-with-a-strong-random-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# For local development (SQLite):
DATABASE_URL=sqlite:///db.sqlite3

# For production (PostgreSQL):
# DATABASE_URL=postgres://user:password@localhost:5432/toriloshop


### Step 4 — Apply Migrations & Collect Static Files

python manage.py migrate
python manage.py collectstatic --noinput


### Step 5 — Run Locally with Gunicorn
gunicorn toriloshop.wsgi:application --bind 127.0.0.1:8000 --workers 3
Then open your browser at: [http://127.0.0.1:8000](http://127.0.0.1:8000)



## Dependencies Summary

| Package | Purpose |
|---------|---------|
| `gunicorn` | Production WSGI server |
| `whitenoise` | Serves static files in production |
| `dj-database-url` | Parses `DATABASE_URL` into Django `DATABASES` config |
| `psycopg2-binary` | PostgreSQL adapter for Python |
| `python-dotenv` | Loads `.env` file into environment variables |

---

## Production Checklist

- `DEBUG=False` in `.env`
- `SECRET_KEY` is strong and not exposed
- `ALLOWED_HOSTS` lists only your actual domain(s)
- `collectstatic` has been run
- Database migrations are up to date
- Gunicorn is running behind Nginx or another reverse proxy



### Screenshots
![gunicorn _running](screenshots/01_gunicorn_running.png)
![collectstatic_output](screenshots/02_collectstatic_output.png)
![requirement_txt](screenshots/03_requirements text.png)
![env_excluded](screenshots/04_gitignore_env_excluded.png)






postgresql://toriloshop_db_k39d_user:MSlTUpu9xFhlgRmL0tFa7q3bRr5tJgDd@dpg-d883crmq1p3s73fse800-a/toriloshop_db_k39d