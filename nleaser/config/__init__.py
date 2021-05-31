import os
from nleaser.config.secure import decrypt

# CONFIGS FLASK
DEBUG = True
SECRET_KEY = decrypt('aIoAE/xxJh6Jgmd4k6x31HEMRkHdp9ZJFSj2AuqMwjNdedqriYQNRZk0Co1FH8KR')
ENV = "development"
HOST = "localhost"
PORT = 5000

# CONFIGS DB
MONGO_HOST = "localhost" #"51.79.63.5"
MONGO_PORT = 27017
MONGO_DB = "nleaser"
MONGO_USER = "nleaser_api"
MONGO_PASSWORD = decrypt('YnBYrdhLu2XVuDiSL9ksGA==')

# CONFIGS JWT
JWT_SECRET_KEY = SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRES = 43200    # 12horas

# CONFIGS RABBIT
RABBIT_HOST = "localhost" #"51.79.63.5"
RABBIT_PORT = 5672