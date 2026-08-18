# Waypoint

A small trail-finder and trip-planner, built as a Django web app on top of a pure-Python domain engine (Weeks 7–8).

## Architecture

Waypoint follows Django's MVT (Model-View-Template) pattern. The domain engine — `Distance`, `Trail` and its subclasses, `Itinerary` — lives in `waypoint_core/`, an importable package that the Django app reuses rather than duplicating logic.

## Setup

1. Clone the repository:

git clone https://github.com/RuchiHP/waypoint.git
cd waypoint


2. Create and activate a virtual environment:

python -m venv env

Windows:

.\env\Scripts\Activate.ps1

macOS/Linux:

source env/bin/activate


3. Install dependencies:

pip install -r requirements.txt


4. Apply migrations:

python manage.py migrate


5. Run the development server:

python manage.py runserver


6. Open http://127.0.0.1:8000/ in your browser.

## Running the domain engine tests

python test_week7.py
python test_week8.py


## Project status

- Week 7: Domain model (Distance, Trail, Itinerary) — done
- Week 8: Trail hierarchy, mixins, operator overloading — done
- Week 9: Django project setup — in progress