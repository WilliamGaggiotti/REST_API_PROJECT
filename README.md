# Ecommerce API
## _Installation and Configuration_

####  _Install virtual environment (optional)_
I recommend that you use some virtual environment to keep your work environment controlled and stable. I personally use anaconda, but you can also opt for other environments like virtualevn, or docker containers.
It remains on your own to choose one and install it.

You can create Anaconda environments with the conda create command. For example, a Python 3 environment called my_env can be created with the following command:
```sh
conda create --name my_env python=3.8
```
Activate the new environment like this:
```sh
conda activate my_env
```

#### _Install dependencies_

Move to the project directory:
```sh
cd  REST_API_PROJECT
```
Install requirements:
```sh
pip install -r requirements.txt
```

#### _Migrate database_

Create and run migrations:
```sh
python manage.py makemigrations
python manage.py migrate
```
#### _Create super user_
The superuser will allow you to manipulate the data manually by hitting the url
localhost/admin
```sh
python manage.py createsuperuser
```

#### _Run the server_
```sh 
python manage.py runserver
```
