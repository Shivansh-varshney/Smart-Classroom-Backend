## Smart Classroom Backend

This is the backend implementation for the Smart Classroom project, developed 
as part of our Software Engineering coursework.

## Project Overview

Our goal is to create a unified platform that brings together all stakeholders in an educational institution, including:

<ul>
    <li>Students</li>
    <li>Teachers</li>
    <li>Administrators</li>
    <li>Parents</li>
</ul>

By integrating various functionalities, we aim to enhance communication, 
streamline academic processes, and improve the overall learning experience.
This backend is designed to be scalable, secure, and efficient, serving as 
the foundation for a modern, technology-driven classroom environment.

> Try command line prototype [here](https://github.com/Shivansh-varshney/School_Management_Project)

## Local setup

> create and run environment
```
virtualenv environment
source environment/bin/activate
```

> install dependencies
```
pip install -r req.txt
```

> to setup postgres locally you can see [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu)

> create .env file inside project directory and set below credentials
```
# database
SQL_USER = ''
SQL_PASSWORD = ''
DATABASE_NAME = ''

# Json Web Token authentication
JWT_ALGORITHM = ''
```

### Get secret key for project
> run django shell
```
python manage.py shell
from django.core.management.utils import get_random_secret_key;
print(get_random_secret_key())
```

> copy and past the secret key in .env file
```
SECRET_KEY = ''
```
