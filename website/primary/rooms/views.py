from trim import views

from . import models

class RoomListView(views.ListView):
    model = models.Room