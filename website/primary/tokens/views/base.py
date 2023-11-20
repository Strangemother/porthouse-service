from trim import views

from .. import models, forms
from trim import get_model
from .json_mixin import ApplicationHeaderJSONSwitchMixin


class TokenCreateView(views.CreateView):
    model = models.Token
    fields = (
        'max_connections',
        'inherit_subscriptions',
        'auto_subscribe',
        )

    def form_valid(self, form):
        form.instance.owner = self.request.user
        res = super().form_valid(form)
        return res

    def get_success_url(self):
        return views.reverse('tokens:list')


class TokenListView(views.ListView):
    model = models.Token


class TokenDetailView(ApplicationHeaderJSONSwitchMixin, views.DetailView):
    model = models.Token

    def as_json_data(self, context, **response_kwargs):
        return {
            "token": context['object'].value
        }


class TokenSubscribeView(views.FormView):
    model = models.Token
    form_class = forms.SubscribeRoomForm
    template_name = 'tokens/token_form.html'
    success_url = views.reverse_lazy('tokens:list')

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        res = self.initial.copy()
        res['token_slug'] = self.kwargs.get('slug')
        return res

    def form_valid(self, form):
        """Create a subscription model between the room and token.
        """
        data = form.cleaned_data

        room = data['room']
        token = models.Token.objects.get(slug=data['token_slug'])
        user = self.request.user

        S = get_model('subscriptions.Subscription')
        sub, c = S.objects.get_or_create(room=room, token=token, creator=user)

        self._report_on(sub, c)
        return super().form_valid(form)

    def _report_on(self, sub, c):
        s = 'collected existing subscription'
        if c:
            s = 'Created a new subscription'
        print(s, sub)

    def get_success_url(self):
        slug = self.kwargs.get('slug')
        return views.reverse('tokens:detail', args=(slug,))


class TokenDeleteView(views.DeleteView):
    model = models.Token
    template_name = 'tokens/delete-form.html'
    success_url = views.reverse_lazy('tokens:list')
