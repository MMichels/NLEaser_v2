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

    @classmethod
    def _from_son(cls, son, _auto_dereference=True, only_fields=None, created=False):
        obj: ConfigModel = super()._from_son(son, _auto_dereference, only_fields, created)
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


def config_rabbit_access():
    user = ConfigModel(
        name="RABBIT_USER",
        cripted=True
    )
    pwd = ConfigModel(
        name="RABBIT_PASS",
        cripted=True
    )
    user.save()
    pwd.save()


if __name__ == '__main__':
    from nleaser.models import connect_db

    connect_db()
    config_rabbit_access()
