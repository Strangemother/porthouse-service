from trim import views

from . import models, forms
from trim import get_model


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

from django.http import JsonResponse


class JSONResponseContent(object):
    json_accept_type = 'application/json'
    json_header_key = 'x-content-type'
    json_method_name = 'as_json_data'

    def render_to_json_response(self, context, **response_kwargs):
        method = getattr(self, self.json_method_name)
        response_data = method(context, **response_kwargs)
        return self.as_json_response(response_data)

    def as_json_response(self, response_data):
        return JsonResponse(response_data)

    def is_ajax_request(self):
        value = self.json_accept_type
        key = self.json_header_key

        return self.request.headers.get(key) == value

    def as_json_data(self, context, **response_kwargs):
        # print('as_json_data')
        return {
            'content': 'json'
        }


class ApplicationHeaderJSONSwitchMixin(JSONResponseContent):
    """An 'application header' switch to detech when the _json_
    content is applex. When the `is_ajax_request` returns True,
    the return is JSON, else the response defaults to the standard GET or
    POST view.

    Apply to the view accepting an optional JSON request:

        class TokenDetailView(ApplicationHeaderJSONSwitchMixin, views.DetailView):
            model = models.Token

            def as_json_data(self, context, **response_kwargs):
                return {
                    "token": context['object'].value
                }
    """
    def render_to_response(self, context, **response_kwargs):
        if self.is_ajax_request():
            return self.render_to_json_response(context, **response_kwargs)
        return super().render_to_response(context, **response_kwargs)



class TokenDetailView(ApplicationHeaderJSONSwitchMixin, views.DetailView):
    model = models.Token

    def as_json_data(self, context, **response_kwargs):
        return {
            "token": context['object'].value
        }



import uuid
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

CSRFTOKENS = set()

@method_decorator(csrf_exempt, name='dispatch')
class TokenInfoFormView(JSONResponseContent, views.FormView):
    model = models.Token
    form_class = forms.TokenExistsForm
    template_name = 'tokens/token_form.html'

    def form_valid(self, form):

        token = form.cleaned_data['token']
        csrftoken = form.cleaned_data['post_token']
        #if self.is_ajax_request():
        if (csrftoken in CSRFTOKENS) is False:
            data = {'ok': False}
            return self.as_json_response(data)

        token = self.model.objects.filter(
                # owner__pk=self.request.user.pk,
                value=token
            ).get()
        data = self._as_response(token)
        return self.as_json_response(data)


    def _as_response(self, token):
        return {
            "value": token.value,
            "owner": token.owner.username,
            "max_connections": token.max_connections,
            "auto_subscribe": token.auto_subscribe,
            "inherit_subscriptions": token.inherit_subscriptions,

        }


@method_decorator(csrf_exempt, name='dispatch')
class TokenExistsView(JSONResponseContent, views.FormView):
    model = models.Token
    form_class = forms.TokenExistsForm
    template_name = 'tokens/token_form.html'

    def form_valid(self, form):

        token = form.cleaned_data['token']
        csrftoken = form.cleaned_data['post_token']
        #if self.is_ajax_request():
        if (csrftoken in CSRFTOKENS) is False:
            data = {'ok': False}
            return self.as_json_response(data)

        print(f'Testing for owner__pk={self.request.user.pk}, value={token}')

        exists = self.model.objects.filter(
                # owner__pk=self.request.user.pk,
                value=token
            ).exists()
        data = {'exists': exists}
        return self.as_json_response(data)

        res = super().form_valid(form)
        return res

    def as_json_data(self, context, **response_kwargs):
        return {
            "exists": True
        }


@method_decorator(csrf_exempt, name='dispatch')
class TokensizerAskFormView(JSONResponseContent, views.FormView):
    """The tokenizer will ask for entry, providing a token.
    If acceptable the form post response with a `post_token`.
    The client tokenizer can use this in future requests as the pseudo csrf_token.

        f=new FormData();
        f.set('token', '4e00a95c-b42d-42ca-9b20-625b6d5f3605');

        fetch('', {
            method: 'POST',
            body:f,
        }).then(request=>request.text()).then(console.log)
    """
    model = models.Token
    form_class = forms.TokenizerMountForm
    template_name = 'tokens/token_form.html'

    def form_valid(self, form):
        token = form.cleaned_data['token']
        post_token = str(uuid.uuid4())
        CSRFTOKENS.add(post_token)

        data = {
            'post_token': post_token
        }

        return self.as_json_response(data)

        # res = super().form_valid(form)
        # return res


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
