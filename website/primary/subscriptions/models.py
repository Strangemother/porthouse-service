from django.db import models
from trim.models import fields, get_model


class Subscription(models.Model):
    _trim_string = 'Subscription "{self.token}" -> "{self.room}" for {self.creator}'

    creator = fields.user_fk(nil=True)
    room  = fields.fk('rooms.Room')
    token = fields.fk('tokens.Token')
    # permissions

    created, updated = fields.dt_cu_pair()
