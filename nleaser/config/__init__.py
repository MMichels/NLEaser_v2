import os
from nleaser.config.secure import decrypt

# CONFIGS FLASK
DEBUG = True
SECRET_KEY = decrypt('KquGQ6P82NnKSyDqbAxFsh5yFbTuNbOoKxepG0fulrvff6pBd7AbyBttmT94YCxI')
ENV = "development"
HOST = "0.0.0.0"
PORT = 5000

# CONFIGS DB
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_TLS = True
MONGO_TLS_INVALID = True
MONGO_DB = "nleaser"
MONGO_USER = "nleaser_api"
MONGO_PASSWORD = decrypt('pcClUU6jksDpoG1ruwUgNw==')

# CONFIGS JWT
JWT_SECRET_KEY = SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRES = 43200    # 12horas

# CONFIGS RABBIT
RABBIT_HOST = "localhost"
RABBIT_PORT = 5672
