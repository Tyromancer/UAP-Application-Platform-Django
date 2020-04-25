# URP-Application-Platform-Django
##### Django version of UAP

## Installation
This installation guide assumes a macOS/Linux environment.

Install virtualenv if you have not already, then activate the virtual python environment
Install the dependencies in the virtual environment by running `python3 -m pip install -r requirements.txt`

Django ships with SQLite3, which this project defaults to. If you want to switch to another database, refer to Django's website for more information.
Set up database by running `python manage.py makemigrations`.
Then run `python manage.py migrate`.

Create super user by running `python manage.py createsuperuser`. You will be able to log in to the admin panel with this super user account.

To set up the email features, set up two environment variables:
- `EMAIL_USER`: Email address
- `EMAIl_PASS`: Application specific password. If you do not know how to set up this, ask your email service provider for help.

The project assumes a Gmail account will be used. To switch to other email providers, change the email settings in `/uap/uap/settings.py`

To start server, cd into /uap and run `python manage.py runserver`.

The website will be up at http://localhost:8000/

You can login to the admin panel as the super user by visiting http://localhost:8000/admin/
---

# TODO:
- [x] Modify styles
- [x] Coding standard for python/django
- [x] Database model for URP listings and projects
- [x] User profile pages
- [x] RTE integration
- [ ] <del>Comments</del>
- [x] URP creation form
- [x] Application features

