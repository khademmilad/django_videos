from django.urls import path
from account.views import (
    home_view,

)

app_name = 'account'

urlpatterns = [
    path('', home_view, name="account_home"),
]