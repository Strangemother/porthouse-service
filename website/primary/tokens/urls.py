from django.urls import include, path, re_path
from trim import urls as t_urls

from . import views


app_name = 'tokens'

urlpatterns = t_urls.paths_named(views,
    list=('TokenListView', ('', 'list/',),),
    create=('TokenCreateView', 'create/'),

    ## API urls.
    ask=('TokensizerAskFormView', 'ask/'),
    info=('TokenInfoFormView', 'info/'),
    exists=('TokenExistsView', 'exists/'),

    detail=('TokenDetailView', 'token/<str:slug>/'),
    delete=('TokenDeleteView', 'token/<str:slug>/delete/'),
    subscribe=('TokenSubscribeView', 'token/<str:slug>/subscribe/'),
)

