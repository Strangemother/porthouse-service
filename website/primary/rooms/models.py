from django.db import models
from trim.models import fields, get_model


class Room(models.Model):
    _trim_string = '{self.name} by {self.owner}'

    owner = fields.user_fk(nil=True)
    name = fields.str(max_length=255)
    max_connections = fields.pos_int(default=50)
    created, updated = fields.dt_cu_pair()
