# Swathi Quiz & Certificate System

A Django web app by **Swathi** for taking online quizzes, saving results, and issuing
verifiable certificates.

## Features
- Enter your name to start (session based)
- Two quizzes: General Knowledge and Web Basics (questions live in `quiz/questions.py`)
- Scores are calculated on the server, so they can't be tampered with in the browser
- Pass mark of 60% earns a printable certificate with a unique ID (e.g. `SW-1A2B3C4D`)
- Certificate verification page
- JSON endpoints: `/results/`, `/results/<student_name>/`, `/summary/`
- Django admin to browse results

## Run locally
```
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser # optional, for /admin/
python manage.py runserver
```
Open http://127.0.0.1:8000/

## Notes
- Set `DJANGO_SECRET_KEY` and `DJANGO_DEBUG=0` for any real deployment.
- The JSON result endpoints are public; add authentication before using real student data.
