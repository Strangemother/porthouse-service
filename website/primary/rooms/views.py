from trim import views

from . import models, forms


class RoomListView(views.ListView):
    model = models.Room


class RoomDetailView(views.DetailView):
    model = models.Room


class DeleteRoomFormView(views.DeleteView):
    # form_class = forms.DeleteRoomForm
    model = models.Room
    template_name = 'rooms/delete-form.html'
    success_url = views.reverse_lazy('rooms:list')


class CreateRoomFormView(views.FormView):
    form_class = forms.CreateRoomForm
    template_name = 'rooms/create-form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        self.room = self.create_room(**data)
        return super().form_valid(form)

    def create_room(self, **kw):
        room = models.Room(
                name=kw['name'],
                owner=self.request.user,
                )
        room.save()
        return room

    def get_success_url(self):
        slug = self.room.slug
        return views.reverse('rooms:detail', args=(str(slug),),)

