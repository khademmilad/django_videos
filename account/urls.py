from django.urls import path
from account.views import (
    home_view,
    register_view,
    login_view,
    logout_view,
    edit_account_view,
    profile_view,

)

app_name = 'account'

urlpatterns = [
    path('', home_view, name="account_home"),
    path('register/',register_view, name="register"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name="logout"),
    path('<user_id>/edit', edit_account_view, name="edit"),
    path('<user_id>/profile/', profile_view, name="profile")
]