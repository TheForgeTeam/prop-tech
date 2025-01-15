# Real Estate Dashboard Setup Instructions

1. Create and activate virtual environment:

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

2. Install required packages:

```bash
pip install django django-tailwind
```

3. Install Node.js:

- Download from nodejs.org
- Install on your system

4. Apply database migrations:

```bash
python manage.py migrate
```

5. Create admin user:

```bash
python manage.py createsuperuser
```

6. Setup Tailwind:

```bash
python manage.py tailwind install
```

7. Run the servers:

# Terminal 1:

```bash
python manage.py runserver
```

# Terminal 2:

```bash
python manage.py tailwind start
```

8. Optional - Create test data:

```bash
python manage.py create_test_data
```

Note: Make sure you have Node.js installed before running the Tailwind commands.
