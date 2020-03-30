# URP-Application-Platform-Django
Django version of UAP
---

## Installation
Install virtualenv if you have not already:
At the root diretory, run `virtualenv .`
To activate the virtual environment, run `. ./bin/activate`.
To quit the environment, run `deactivate`
To install the dependencies, run `python3 -m pip install -r requirements.txt`


Set up database by running `python manage.py makemigrations`
Then run `python manage.py migrate`

Create super user: `python manage.py createsuperuser`

To start server, cd into /uap and run `python manage.py runserver`
The server will be up at http://localhost:8000/
You can login to the admin panel as the super user by visiting http://localhost:8000/admin/
---

# TODO:
- [ ] Modify styles
- [x] Coding standard for python/django
- [x] Database model for URP listings and projects
- [ ] User profile pages
- [x] RTE integration
- [ ] <del>Comments</del>
- [x] URP creation form
- [ ] Application features

