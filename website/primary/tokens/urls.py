from django.urls import include, path, re_path
from trim import urls as t_urls

from . import views


app_name = 'tokens'

urlpatterns = t_urls.paths_named(views,
    ## Frontend user access
    list=('TokenListView', ('', 'list/',),),
    create=('TokenCreateView', 'create/'),

    ## API urls.
    ### Token info
    ask=('TokensizerAskFormView', 'ask/'),
    info=('TokenInfoFormView', 'info/'),
    exists=('TokenExistsView', 'exists/'),
    ### User info
    user_detail=('AccountTokenDetailView', 'user/'),

    ## Frontend user access
    detail=('TokenDetailView', 'token/<str:slug>/'),
    delete=('TokenDeleteView', 'token/<str:slug>/delete/'),
    subscribe=('TokenSubscribeView', 'token/<str:slug>/subscribe/'),

)

