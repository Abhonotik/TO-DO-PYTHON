from django.urls import path
from .views import signup_view, login_view, logout_view, todo_view, home_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('todo/', todo_view, name='todo'),
    path("", home_view, name="home"),
]

