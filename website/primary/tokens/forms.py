from django import forms
from trim.forms import fields
from trim.models import get_model


class SubscribeRoomForm(forms.Form):
    token_slug = fields.chars(max_length=255, required=True)
    room = fields.modelchoice(get_model('rooms.room').objects.all())


class TokenExistsForm(forms.Form):
    token = fields.chars(max_length=255, required=True)
    post_token = fields.chars(max_length=255, required=True)

class TokenInfoForm(forms.Form):
    token = fields.chars(max_length=255, required=True)
    post_token = fields.chars(max_length=255, required=True)


class TokenizerMountForm(forms.Form):
    token = fields.chars(max_length=255, required=True)
