# URP-Application-Platform-Django
Django version of UAP
---

## Installation
Install virtualenv if you have not already
At the root diretory, run `virtualenv .`
To activate the virtual environment, run `. ./bin/activate`. To quit the environment, run `deactivate`
Install the following packages in venv:
- django
- pillow
- django-crispy-forms

Set up database by running `python manage.py makemigrations`
Then `python manage.py migrate`

Create super user: `python manage.py createsuperuser`

To start server, cd into /uap and run `python manage.py runserver`
The server will be up at http://localhost:8000/
You can login to the admin panel as the super user by visiting http://localhost:8000/admin/


# TODO:
[ ] Modify styles
[ ] Coding standard for python/django
[ ] Database model for URP listings and projects
[ ] User profile pages
[ ] RTE integration
[ ] Comments
[ ] URP creation form

