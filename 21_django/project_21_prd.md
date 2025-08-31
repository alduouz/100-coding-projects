# Project 21: Basic Django App - PRD

## Overview
Set up a minimal Django project with one app and display a simple “Hello, World” page.

## Functional Requirements
- Install Django in a virtual environment.
- Create a new Django project (`django-admin startproject mysite`).
- Create a new app (`python manage.py startapp hello`).
- Add the app to `INSTALLED_APPS` in `settings.py`.
- Define a single view in `views.py` that returns "Hello, World".
- Configure `urls.py` so that `/` maps to the hello view.
- Run the Django development server and confirm page loads.

## Non-Functional Requirements
- Use Python 3.x and the latest stable Django version.
- Code should follow PEP8 standards.
- Project should be runnable on localhost without extra setup.

## User Story
**As a developer**, I want to create a basic Django app that displays “Hello, World” so that I understand Django’s project/app structure and URL routing.

## Acceptance Criteria
- [ ] A Django project named `mysite` exists.
- [ ] An app named `hello` is created and registered in `INSTALLED_APPS`.
- [ ] Visiting `http://127.0.0.1:8000/` displays “Hello, World”.
- [ ] Screenshot of working browser output is provided.
- [ ] `views.py` and `urls.py` source files are submitted.

## Deliverables
- Screenshot of "Hello, World" running in browser.
- `views.py` and `urls.py` code files.
- PRD document (this file).

## Lesson
- Understand Django’s project vs. app structure.
- Learn URL routing and views.
- Run and test Django dev server.

