import datetime
import mongoengine as me
from nleaser.config.secure import crypt, decrypt


class ConfigModel(me.Document):
    meta = {
        "allow_inheritance": True,
        "collection": "config"
    }

    name = me.fields.StringField(required=True)
    value = me.fields.StringField(required=True)
    cripted = me.fields.BooleanField(default=False)
    created_at = me.fields.DateTimeField(default=datetime.datetime.now)
    changed_at = me.fields.DateTimeField()

    def __getitem__(self, item):
        if item == 'value' and self.cripted:
            return decrypt(self.value)
        else:
            return super().__getitem__(item)

    def _from_son(cls, son, _auto_dereference=True, only_fields=None, created=False):
        obj: ConfigModel = super()._from_son()
        if obj.cripted:
            obj.value = decrypt(obj.value)

        return obj

    def save(self, force_insert=False, validate=True,
             clean=True, write_concern=None, cascade=None, cascade_kwargs=None,
             _refs=None, save_condition=None, signal_kwargs=None, **kwargs):

        if self.cripted:
            self.value = crypt(self.value)

        self.changed_at = datetime.datetime.now()

        self = super(ConfigModel, self).save(force_insert, validate, clean,
                                             write_concern, cascade, cascade_kwargs,
                                             _refs, save_condition, signal_kwargs, **kwargs)

        return self


if __name__ == '__main__':
    from nleaser.models import connect_db

    connect_db()

    while True:
        name = input("Nome da config: ")
        value = input("Valor: ")
        cripted = input("Criptografar? (s/n)").lower()[0] == 's'

        cfg = ConfigModel(
            name=name,
            value=value,
            cripted=cripted
        )

        try:
            cfg.save()
            print("Salvo!")
        except Exception as ex:
            print("Erro ao salvar: ", ex)

        interromper = input("Continuar? (s/n)").lower()[0] == 'n'
        if interromper:
            break

