from django.db import models
from trim.models import fields, get_model


class Token(models.Model):

    _trim_string = 'Token "{self.value}" for {self.owner}'

    owner = fields.user_fk(nil=True)
    value = fields.str_uuid()
    max_connections = fields.pos_int(default=10)
    inherit_subscriptions = fields.bool_false()
    auto_subscribe = fields.bool_false()
    created, updated = fields.dt_cu_pair()
