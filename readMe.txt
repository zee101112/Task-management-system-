python -m venv myenv
myenv\Scripts\activate

packages to be installed

pip install django
python -m pip install Pillow

create the django project
django-admin startproject core .
cd core

create the django app 
django-admin startapp TMapp

Run DB migrations (initial setup)
python manage.py migrate

(Models you will create in the project)

python manage.py makemigrations TMapp
python manage.py migrate 


create superuser

python manage.py createsuperuser
i have
email
firstname
lastname
pass
y (bypass password validation)

add token in the user_profile table manually
0768aca3-69b1-49aa-9852-c8894da4ee12 against user_id reference to login with the created admin account bby django command
run the project
python manage.py runserver

{to access django given admin panel}
http://127.0.0.1:8000/admin (django admin panel)
http://127.0.0.1:8000/  (static page)

