from trim import views

from .. import models, forms
from trim import get_model

import uuid
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

from .json_mixin import JSONResponseContent


# CSRFTOKENS = set()
from .token_cache import CSRFTOKENS

@method_decorator(csrf_exempt, name='dispatch')
class TokenInfoFormView(JSONResponseContent, views.FormView):
    """Token information through an endpoint, validated through a POST
    including the post_token and user 'token'.

    CSRF Exempt
    """
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


