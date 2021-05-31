from nleaser.config.secure import decrypt

# CONFIGS FLASK
DEBUG = True
SECRET_KEY = "" +\
ENV = "development"
HOST = "localhost"
PORT = 5000

# CONFIGS DB
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "nleaser"
MONGO_TLS = True
MONGO_TLS_INVALID = True
MONGO_USER = "" +\
MONGO_PASSWORD = "" +\

# CONFIGS JWT
JWT_SECRET_KEY = SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRES = 43200    # 12horas

# CONFIGS RABBIT
RABBIT_HOST = "localhost"
RABBIT_PORT = 5672



