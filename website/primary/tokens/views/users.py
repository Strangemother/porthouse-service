from trim import views

from .. import models, forms
from django.utils.decorators import method_decorator
from trim import get_model
from django.views.decorators.csrf import csrf_exempt
from .json_mixin import ApplicationHeaderJSONSwitchMixin

from .token_cache import CSRFTOKENS


@method_decorator(csrf_exempt, name='dispatch')
class AccountTokenDetailView(ApplicationHeaderJSONSwitchMixin, views.FormView):
    model = get_model('account.Account')
    form_class = forms.TokenExistsForm
    template_name = 'tokens/token_form.html'

    def form_valid(self, form):

        token = form.cleaned_data['token']
        #print('valid form for token', token)
        csrftoken = form.cleaned_data['post_token']
        #if self.is_ajax_request():
        if (csrftoken in CSRFTOKENS) is False:
            data = {'ok': False}
            print('token is not in CSRFTOKENS', csrftoken)
            return self.as_json_response(data)

        accounts = self.model.objects.filter(
                # owner__pk=self.request.user.pk,
                user__token__value=token
            )
        # Where token is assigned to rooms
        Subscription = get_model('subscriptions.subscription')
        sub_models = Subscription.objects.filter(
                    token__value=token
                )
        subs = {x.room.name: {} for x in sub_models}
        print('subs', subs)
        if accounts.exists():
            account = accounts.get()
        else:
            print(f'No result for {token=}', accounts)
        # data = { 'user': account.user.username }
        return self.as_json_response(self._as_json_data(account, subs))


    def _as_json_data(self, account, subs, **response_kwargs):
        return {
            "username": account.user.username,
            "subscriptions": subs,
            **response_kwargs
        }


