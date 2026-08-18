# Waypoint

A trail-finder and trip-planner built as an individual term project (Weeks 7-14), combining a pure-Python domain engine with a Django web app.

## Architecture

Waypoint follows Django's MVT (Model-View-Template) pattern. The domain engine — `Distance`, `Trail` and its subclasses, `Itinerary` — lives in `waypoint_core/`, an importable package used for the domain-level unit tests. The web app stores trail data in a `Trail` model (with a `Park` ForeignKey relationship) inside the `trails` app, and serves `home`, `report`, `search`, and `catalog`-style pages through the `core` and `trails` apps.

## Setup

1. Clone the repository:

git clone https://github.com/RuchiHP/waypoint.git
cd waypoint

2. Create and activate a virtual environment:

python -m venv env
env\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt

4. Run migrations:

python manage.py migrate

5. (Optional) Create a superuser for the admin site:

python manage.py createsuperuser

6. Run the development server:

python manage.py runserver

7. Visit http://127.0.0.1:8000/

## Pages

- `/` — Home
- `/report/` — Trail report form (CSRF-protected)
- `/search/` — Search
- `/trails/` — Trail catalog (database-backed, open trails only, sorted by distance)
- `/trails/park/<id>/` — Trails filtered by park
- `/admin/` — Django admin (manage Trails and Parks)

## Running tests

python manage.py test


## Known issue

The Django admin **add/edit form** for Trail currently fails locally on this machine due to a Python 3.14 / Django 4.2 template-context compatibility bug (Django 4.2 officially supports Python up to 3.12). The admin **dashboard and list views work correctly**. Trail/Park records can be created via `python manage.py shell` as a workaround; the model, admin registration (`list_display`, `search_fields`), and public-facing views all function correctly.

## Project status

- Week 7: Domain model (Distance, Trail, Itinerary) — done
- Week 8: Trail hierarchy, mixins, operator overloading — done
- Week 9: Django project setup — done
- Week 10: Views, URLs, report form — done
- Week 11: Base template, partials, trail catalog — done
- Week 12: Trail model, admin, database-backed catalog — done
- Week 13: Park model, ForeignKey relationship — done
- Week 14: Testing and handoff — done