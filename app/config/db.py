import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# psycopg2

POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'liga',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

# mysqlclient

MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'liga',
        'USER': 'root',
        'PASSWORD': '$Lenovo01',
        'HOST': 'localhost',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True
    }
}

PROD = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'liga',
        'USER': 'useradd',
        'PASSWORD': '$Lenovo01',
        'HOST': 'prod.cmhemg9uamjj.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True
    }
}
