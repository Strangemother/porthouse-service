from django import forms
from trim.forms import fields


class CreateRoomForm(forms.Form):
    name = fields.chars(max_length=255, required=True)
    public = fields.bool_false()
    # message = fields.text(required=True) # A ready-to-go CharField with a TextArea widget