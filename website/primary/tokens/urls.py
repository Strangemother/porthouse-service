from django.urls import include, path, re_path
from trim import urls as t_urls

from . import views


app_name = 'tokens'

urlpatterns = t_urls.paths_named(views,
    list=('TokensListView', ('', 'list/',),),
)

