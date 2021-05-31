from mongoengine import connect
from pymongo import MongoClient

from nleaser.config import MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_USER, MONGO_PASSWORD, MONGO_TLS, MONGO_TLS_INVALID


def connect_db():
    connection: MongoClient = connect(
        db=MONGO_DB,
        host=MONGO_HOST,
        port=MONGO_PORT,
        username=MONGO_USER,
        password=MONGO_PASSWORD,
        authentication_source=MONGO_DB,
        tls=MONGO_TLS,
        tlsAllowInvalidCertificates=MONGO_TLS_INVALID
    )
    db = connection.get_default_database(MONGO_DB)
    assert db.name == MONGO_DB, "Erro ao conectar no banco de dados, database " + MONGO_DB + " não encontrada"
