from trim import views

from . import models

class TokensListView(views.ListView):
    model = models.Token